MODEL_PATH="your model path"
SAVE_PATH="save path"
MODEL_ID="your model name"
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

cd vllm-main/examples/csbench
bash ./gen_model_answer_en.sh \
        --model-path $MODEL_PATH \
        --save-path $SAVE_PATH \
        --model-id $MODEL_ID \
        --prompt_prefix "[INST]" \
        --prompt_suffix "[/INST]" \
        --tp 8
# # &&
bash ./gen_model_answer_cn.sh \
        --model-path $MODEL_PATH \
        --save-path $SAVE_PATH \
        --model-id $MODEL_ID \
        --prompt_prefix "[INST]" \
        --prompt_suffix "[/INST]" \
        --tp 8

