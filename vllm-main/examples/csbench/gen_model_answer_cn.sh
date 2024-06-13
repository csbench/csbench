
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model-path) MODEL_PATH="$2"; shift ;;
        --save-path) SAVE_PATH="$2"; shift ;;
        --model-id) MODEL_ID="$2"; shift ;;
        --prompt_prefix) prompt_prefix="$2"; shift ;;
        --prompt_suffix) prompt_suffix="$2"; shift ;;
        --tp) tp="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


# 使用传入的参数构建完整的 save_path
full_save_path="${SAVE_PATH}/${MODEL_ID}"

# 运行 python 脚本
python3 ./gen_model_answer_cn.py \
--tp=$tp \
--data-path=../../../data/cn_test.json \
--model-path=$MODEL_PATH \
--save-path=$full_save_path \
--prompt-prefix "$prompt_prefix" \
--prompt-suffix "$prompt_suffix"


