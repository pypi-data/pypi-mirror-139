import torch
import numpy as np
import torchgeometry
import torchvision

from hcai_models.expansion.preprocessing.bounding_box_image_crop import (
    BoundingBoxImageCrop,
)
from hcai_models.models.image.hcai_blaze_face.blaze_face import BlazeFace

# TODO Mabye it's better to separate boundingbox caluclation and crop?
class PyTorchFaceCrop:
    def __init__(
            self, min_score_thres: float = 0.7, output_dim=(256, 256), device="cuda"
    ):
        self.device = device
        self.min_score_thres = min_score_thres
        self.detector = BlazeFace(weights="ls3d-w", min_score_thres=min_score_thres)
        self.detector.build_model()
        self.detector._model.to(self.device)
        self.output_dim = output_dim
        self.reference_scale = self.detector.reference_scale

    def __call__(self, image_original, *args, **kwargs):

        input_img = torchvision.transforms.Resize(size=(128, 128))(image_original)

        # calculate some shifts for back-projecting the box on the original image
        orig_size_y = image_original.size(dim=-1)
        orig_size_x = image_original.size(dim=-2)
        orig_size = min(orig_size_y, orig_size_x)
        if orig_size_x > orig_size_y:
            yshift, xshift = (orig_size_x - orig_size_y) // 2, 0
        else:
            yshift, xshift = 0, (orig_size_y - orig_size_x) // 2

        # 2. Run the neural network:
        with torch.no_grad():
            out = self.detector._model(input_img)

        # 3. Postprocess the raw predictions:
        detections = self.detector._model._tensors_to_detections(
            out[0], out[1], self.detector._model.anchors
        )

        # 4. Apply weighted non-maximum suppression to remove overlapping detections:
        prediction = []
        for i in range(len(detections)):
            faces = self.detector._model._weighted_non_max_suppression(detections[i])
            faces = torch.stack(faces) if len(faces) > 0 else torch.zeros((0, 17))
            prediction.append(faces)

        prediction = prediction[0]
        shift = np.array([xshift, yshift] * 2)
        scores = prediction[:, -1:]
        locs = np.concatenate(
            (
                prediction[:, 1:2],
                prediction[:, 0:1],
                prediction[:, 3:4],
                prediction[:, 2:3],
            ),
            axis=1,
        )

        detected_faces = np.concatenate((locs * orig_size + shift, scores), axis=1)
        if detected_faces.shape[0] != 0:
            detected_faces = detected_faces[0]
        else:
            return torchvision.transforms.Resize(size=self.output_dim)(image_original)

        return self._crop(image_original, detected_faces)

    def _crop(self, image, bbox, *args, **kwargs):

        if bbox[-1] == 0.0:
            # face not found -> fall back to original image
            scale, center = 1.0, np.array([image.shape[1] / 2, image.shape[0] / 2])
        else:
            center = np.array([bbox[2] - (bbox[2] - bbox[0]) / 2, bbox[3] - (bbox[3] - bbox[1]) / 2])
            scale = (bbox[2] - bbox[0] + bbox[3] - bbox[1]) / self.reference_scale

        # Generate transformation matrix
        h = 200 * scale
        # t = np.zeros((3, 3))
        t = torch.full((3, 3), 0, device=self.device, dtype=torch.float32)
        t[0, 0] = float(self.output_dim[1]) / h
        t[1, 1] = float(self.output_dim[0]) / h
        t[0, 2] = self.output_dim[1] * (-float(center[0]) / h + 0.5)
        t[1, 2] = self.output_dim[0] * (-float(center[1]) / h + 0.5)
        t[2, 2] = 1
        # t = torch.tensor(t, device=self.device, dtype=torch.float32)

        # image = torch.swapaxes(image, 0, 2).unsqueeze(0) / 255
        image = torchgeometry.warp_perspective(image, t, self.output_dim)

        return image
