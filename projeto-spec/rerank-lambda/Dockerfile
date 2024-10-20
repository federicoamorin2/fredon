FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy all files in ./src
COPY artifacts/ ${LAMBDA_TASK_ROOT}/artifacts/ 
COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY app.py ${LAMBDA_TASK_ROOT} 

ENV HF_HOME='/tmp/huggingface/hub/'
# Set the CMD to your handler.
CMD [ "app.handler" ]