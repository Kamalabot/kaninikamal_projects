import shlex
import subprocess

import gradio as gr
import numpy as np
import spaces
import torch
from diffusers import DiffusionPipeline

subprocess.run(
    shlex.split(
        "pip install https://huggingface.co/spaces/dylanebert/LGM-mini/resolve/main/wheel/diff_gaussian_rasterization-0.0.0-cp310-cp310-linux_x86_64.whl"
    )
)

pipeline = DiffusionPipeline.from_pretrained(
    "dylanebert/LGM-full",
    custom_pipeline="dylanebert/LGM-full",
    torch_dtype=torch.float16,
    trust_remote_code=True,
).to("cuda")


@spaces.GPU
def run(image):
    input_image = np.array(image, dtype=np.float32) / 255.0
    splat = pipeline(
        "", input_image, guidance_scale=5, num_inference_steps=30, elevation=0
    )
    splat_file = "/tmp/output.ply"
    pipeline.save_ply(splat, splat_file)
    return splat_file


demo = gr.Interface(
    fn=run,
    title="LGM Tiny",
    description="An extremely simplified version of [LGM](https://huggingface.co/ashawkey/LGM). Intended as resource for the [ML for 3D Course](https://huggingface.co/learn/ml-for-3d-course/unit0/introduction).",
    inputs="image",
    outputs=gr.Model3D(),
    examples=[
        "https://huggingface.co/datasets/dylanebert/iso3d/resolve/main/jpg@512/a_cat_statue.jpg"
    ],
    cache_examples=True,
    allow_duplication=True,
)
demo.queue().launch()
