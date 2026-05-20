FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Set cache locations for Lambda
ENV HOME=/tmp
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/tmp/huggingface
ENV TORCH_HOME=/tmp/torch

COPY chatbot_api.py .
COPY chatbot.py .
COPY faq_data.json .

CMD ["chatbot_api.handler"]