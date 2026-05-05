pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'username_anda'
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
                
                withCredentials([usernamePassword(credentialsId: 'docker-hub-login', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/frontend:latest"
                    sh "docker push ${DOCKER_HUB_USER}/backend:latest"
                }
            }
        }
        stage('Deploy to AKS') {
            steps {
                // Menggunakan kubeconfig yang sudah dikonfigurasi di Jenkins
                sh "kubectl apply -f k8s/backend-deployment.yaml"
                sh "kubectl apply -f k8s/frontend-deployment.yaml"
                sh "kubectl apply -f k8s/ingress.yaml"
                
                // Rollout restart agar image terbaru segera ditarik
                sh "kubectl rollout restart deployment/backend-deployment"
                sh "kubectl rollout restart deployment/frontend-deployment"
            }
        }
    }
}