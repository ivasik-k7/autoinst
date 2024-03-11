import torch
from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from diffusers import (
    DiffusionPipeline,
    StableDiffusionPipeline,
    DPMSolverMultistepScheduler,
    StableDiffusionXLImg2ImgPipeline,
    EulerDiscreteScheduler,
    StableDiffusionImg2ImgPipeline,
)


class DiffusionStrategy(ABC):
    @abstractmethod
    def pipeline(self, *args, **kwargs) -> DiffusionPipeline:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> List[Image.Image]:
        pass


class GeneratorStrategy(DiffusionStrategy):
    def pipeline(
        self,
        model_id,
        use_safetensors=True,
    ) -> DiffusionPipeline:

        device = "cuda" if torch.cuda.is_available() else "cpu"

        scheduler = DPMSolverMultistepScheduler.from_pretrained(
            model_id, subfolder="scheduler"
        )
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            scheduler=scheduler,
            torch_dtype=torch.float32,
            use_safetensors=use_safetensors,
        )

        pipe = pipe.to(device)

        return pipe

    def execute(
        self,
        pipeline,
        prompt: str,
        negative_prompt: str,
        high_noise_frac: float,
        num_inference_steps: int,
        num_images_per_prompt: int,
        width: int,
        height: int,
    ) -> List[Image.Image]:

        result = pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            denoising_end=high_noise_frac,
            num_inference_steps=num_inference_steps,
            num_images_per_prompt=num_images_per_prompt,
        ).images

        return result


class RefinerStrategy(DiffusionStrategy):
    def pipeline(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-refiner-1.0",
        use_safetensors=True,
    ) -> DiffusionPipeline:
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
        scheduler = EulerDiscreteScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
        )
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            scheduler=scheduler,
            torch_dtype=torch.float32,
            use_safetensors=use_safetensors,
        )
        pipe = pipe.to(device)

        return pipe

    def execute(
        self,
        pipeline,
        image: Image,
        prompt: str,
        negative_prompt: str,
        high_noise_frac: float,
        num_inference_steps: int,
        num_images_per_prompt: int,
        width: int,
        height: int,
    ) -> List[Image.Image]:
        return pipeline(
            prompt=prompt,
            image=image,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            denoising_end=high_noise_frac,
            num_inference_steps=num_inference_steps,
            num_images_per_prompt=num_images_per_prompt,
        ).images
