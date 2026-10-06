#!/bin/bash
#SBATCH --job-name=trimen-qwen
## no --partition: plato routes by --gres (see tropical/parse/plato_classify.slurm)
#SBATCH --gres=gpu:3g.40gb:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=01:30:00
#SBATCH --output=%x-%j.out
#
# Run C for the workshop: the two extraction prompts against Qwen3.8-27B-FP8 served by vLLM,
# once with thinking off and once with thinking on. Serving block copied from
# tropical/parse/plato_classify.slurm, which is known to work on a 3g.40gb slice.
set -euo pipefail
C50=${C50:-$HOME/projects/canada50}
W=${W:-/project/clifford/trimen_workshop}
MODEL_DIR=${MODEL_DIR:-$C50/models/Qwen3.8-27B-FP8}
SIF=${SIF:-$C50/containers/vllm.sif}
MODEL_NAME=${MODEL_NAME:-Qwen/Qwen3.8-27B-FP8}
MAXLEN=${MAXLEN:-40960}
PORT=${PORT:-8137}

echo "node $(hostname)  job $SLURM_JOB_ID  $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
export HF_HUB_OFFLINE=1 HF_HOME=$C50/hf_cache VLLM_LOGGING_LEVEL=WARNING
module load apptainer/1.4.5 2>/dev/null || module load apptainer 2>/dev/null || true
CTR=$(command -v apptainer || command -v singularity)
export APPTAINERENV_HF_HUB_OFFLINE=1 APPTAINERENV_HF_HOME=$C50/hf_cache
RUN=("$CTR" exec --nv --bind "$C50":"$C50" --bind "$W":"$W" "$SIF" python3)
CLI=("$CTR" exec --bind "$W":"$W" "$SIF" python3)

"${RUN[@]}" -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_DIR" --served-model-name "$MODEL_NAME" \
    --port "$PORT" --host 127.0.0.1 \
    --max-model-len "$MAXLEN" --gpu-memory-utilization "${GPU_UTIL:-0.93}" \
    --max-num-seqs 4 --limit-mm-per-prompt '{"image":0,"video":0}' \
    > "$W/vllm-$SLURM_JOB_ID.log" 2>&1 &
VLLM_PID=$!
trap 'kill $VLLM_PID 2>/dev/null || true' EXIT INT TERM
for i in $(seq 1 180); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/v1/models" || echo 000)
    [ "$code" = "200" ] && { echo "server up after ${i}x5s"; break; }
    kill -0 $VLLM_PID 2>/dev/null || { echo "SERVER DIED"; tail -30 "$W/vllm-$SLURM_JOB_ID.log"; exit 1; }
    sleep 5
done

echo "--- run C (thinking off) $(date -Is)"
"${CLI[@]}" "$W/02_extract.py" --base-url "http://127.0.0.1:$PORT/v1" --model "$MODEL_NAME" \
    --sources "$W/sources" --out "$W/out/C-nothink"
echo "--- run C (thinking on) $(date -Is)"
"${CLI[@]}" "$W/02_extract.py" --base-url "http://127.0.0.1:$PORT/v1" --model "$MODEL_NAME" \
    --sources "$W/sources" --out "$W/out/C-think" --thinking
echo "done $(date -Is)"
