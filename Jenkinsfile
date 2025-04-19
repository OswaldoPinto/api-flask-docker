pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mi-api-flask'
        DOCKER_TAG = 'latest'
        DOCKER_REGISTRY = 'docker.io'
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
                    sh 'docker build -t $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Empujar Imagen a DockerHub') {
            steps {
                echo 'Empujando imagen a DockerHub...'
                script {
                    // Login a DockerHub, si es necesario
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Ejecutar Contenedor Docker') {
            steps {
                echo 'Ejecutando el contenedor Docker...'
                script {
                    sh 'docker run -d -p 5000:5000 --name $DOCKER_IMAGE $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG'
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
            // Limpiar el contenedor después de cada ejecución
            sh 'docker ps -q -f "name=$DOCKER_IMAGE" | grep -q . && docker stop $DOCKER_IMAGE && docker rm $DOCKER_IMAGE'
        }
    }
}

