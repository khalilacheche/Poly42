import sys
import logging

import datasets
from datasets import load_dataset
from peft import LoraConfig
import torch
import transformers
from trl import DPOTrainer, DPOConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)


logger = logging.getLogger(__name__)


###################
# Hyper-parameters
###################
peft_config = {
    "r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM",
    "target_modules": ["o_proj", "qkv_proj", "gate_up_proj", "down_proj"],
    "modules_to_save": None,
}
peft_conf = LoraConfig(**peft_config)


###############
# Setup logging
###############
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log_level = logging.INFO
logger.setLevel(log_level)
datasets.utils.logging.set_verbosity(log_level)
transformers.utils.logging.set_verbosity(log_level)
transformers.utils.logging.enable_default_handler()
transformers.utils.logging.enable_explicit_format()

# Log on each process a small summary
logger.info(f"PEFT parameters {peft_conf}")


################
# Model Loading
################
checkpoint_path = "microsoft/Phi-3-mini-4k-instruct"
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)
model_kwargs = dict(
    use_cache=False,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    device_map=None,
    quantization_config=quantization_config,
)
model = AutoModelForCausalLM.from_pretrained(checkpoint_path, **model_kwargs)
print(model)
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
tokenizer.model_max_length = 2048
tokenizer.pad_token = (
    tokenizer.unk_token
)  # use unk rather than eos token to prevent endless generation
tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
tokenizer.padding_side = "right"

dpo_args = DPOConfig(
    output_dir="./checkpoints",
    beta=0.1,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    do_eval=True,
)


dataset = load_dataset(
    "json",
    data_files={
        "train": "datasets/train_dataset.jsonl",
        "eval": "datasets/eval_dataset.jsonl",
    },
)

train_dataset = dataset["train"]


eval_dataset = dataset["eval"]


print("dataset loaded")

###########
# Training
###########
trainer = DPOTrainer(
    model=model,
    args=dpo_args,
    peft_config=peft_conf,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)
train_result = trainer.train()
metrics = train_result.metrics
trainer.log_metrics("train", metrics)
trainer.save_metrics("train", metrics)
trainer.save_state()


#############
# Evaluation
#############
tokenizer.padding_side = "right"
metrics = trainer.evaluate()
metrics["eval_samples"] = len(eval_dataset)
trainer.log_metrics("eval", metrics)
trainer.save_metrics("eval", metrics)


# ############
# # Save model
# ############
trainer.save_model("./checkpoints")
