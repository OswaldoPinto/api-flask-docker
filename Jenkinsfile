pipeline {
    agent any

    stages {
        stage('Clonar Repositorio') {
            steps {
                echo 'Clonando el repositorio...'
            }
        }

        stage('Construir Imagen Docker') {
            steps {
                script {
                    echo 'Construyendo imagen Docker...'
                    sh 'docker build -t mi-api-flask .'
                }
            }
        }

        stage('Finalizado') {
            steps {
                echo 'Pipeline completado 🎉'
            }
        }
    }
}

