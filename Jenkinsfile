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
                withKubeConfig([credentialsId: 'k8s-config']) {
                    // 1. Jalankan semua file manifest di folder k8s (termasuk ingress.yaml)
                    sh 'kubectl apply -f k8s/'
                    
                    // 2. PAKSA RESTART agar variabel NAMA/NIM terbaru terinjeksi
                    sh 'kubectl rollout restart deployment tcg-frontend'
                    sh 'kubectl rollout restart deployment tcg-backend'
                    
                    // 3. Pastikan Ingress Controller terinstal (Opsional, untuk jaga-jaga)
                    sh 'kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml'
                }
            }
        }
    }
}