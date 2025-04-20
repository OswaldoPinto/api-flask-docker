pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '203918886396'
        ECR_REPO_NAME = 'mini-blog-backend'
        DOCKER_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                echo 'Clonando el repositorio...'
                git url: 'https://github.com/OswaldoPinto/api-flask-docker.git', branch: 'main'
            }
        }

        stage('Construir Imagen Docker') {
            steps {
                echo 'Construyendo imagen Docker...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Login a Amazon ECR') {
            steps {
                echo 'Autenticándose en Amazon ECR...'
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                }
            }
        }

        stage('Empujar Imagen a Amazon ECR') {
            steps {
                echo 'Empujando imagen a Amazon ECR...'
                script {
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Ejecutar Contenedor Docker') {
            steps {
                echo 'Ejecutando el contenedor desde imagen ECR...'
                script {
                    sh "docker run -d -p 5000:5000 --name mi-api-ecr ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Finalizado') {
            steps {
                echo 'Pipeline completado 🎉'
            }
        }
    }

    post {
        always {
            // Limpiar el contenedor anterior
            sh 'docker ps -q -f "name=mi-api-ecr" | grep -q . && docker stop mi-api-ecr && docker rm mi-api-ecr || true'
        }
    }
}

