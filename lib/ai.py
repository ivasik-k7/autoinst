import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


class DiffusionGenerator:
    @staticmethod
    def load_diffusion_pipeline(
        model_id,
        use_safetensors=True,
    ):
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            use_safetensors=use_safetensors,
        )

        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

        return pipe

    @staticmethod
    def generate_images(
        *,
        pipeline,
        prompt: str,
        negative_prompt: str,
        high_noise_frac: float,
        num_inference_steps: int,
        num_images_per_prompt: int,
        width: int,
        height: int,
    ):
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
