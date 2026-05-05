pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'abdillah11'
        APP_NAME = 'tcg-app'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/trexvolution/tcg-collector.git'
            }
        }
        stage('Build & Push') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/frontend:latest ./frontend"
                sh "docker build -t ${DOCKER_HUB_USER}/backend:latest ./backend"
                
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/frontend:latest"
                    sh "docker push ${DOCKER_HUB_USER}/backend:latest"
                }
            }
        }
        stage('Deploy to AKS') {
            steps {
            // ID 'k8s-config' harus sesuai dengan ID yang Anda buat di Jenkins Credentials
            withKubeConfig([credentialsId: 'k8s-config']) {
            sh 'kubectl apply -f k8s/backend-deployment.yaml'
            sh 'kubectl apply -f k8s/frontend-deployment.yaml'
                }
            }
        }
    }
}