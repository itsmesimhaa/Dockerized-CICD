pipeline {
    agent any

    environment {
        FRONTEND_IMAGE = 'itsmesimha/frontend-nginx'
        BACKEND_IMAGE = 'itsmesimha/backend-flask'
    }

    stages {
        stage('Clone Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'gitHub-credentials', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                    git branch: 'main', credentialsId: 'gitHub-credentials', url: "https://$GITHUB_USER:$GITHUB_TOKEN@github.com/itsmesimhaa/Dockerized-CICD.git"
                }
            }
        }

        stage('Build and Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Docker-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                    script {
                        sh """
                        docker build -t $FRONTEND_IMAGE:latest frontend/
                        docker build -t $BACKEND_IMAGE:latest backend/
                        
                        echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin
                        docker push $FRONTEND_IMAGE:latest
                        docker push $BACKEND_IMAGE:latest
                        docker logout
                        """
                    }
                }
            }
        }
        stage('Update Kubernetes Manifests') {
    steps {
        script {
            sh "sed -i 's|image: itsmesimha/frontend-nginx:.*|image: itsmesimha/frontend-nginx:${BUILD_NUMBER}|' frontend-deployment.yaml"
            sh "sed -i 's|image: itsmesimha/backend-flask:.*|image: itsmesimha/backend-flask:${BUILD_NUMBER}|' backend-deployment.yaml"

            sh 'git config --global user.email "your-email@example.com"'
            sh 'git config --global user.name "your-github-username"'
            sh 'git add frontend-deployment.yaml backend-deployment.yaml'
            sh 'git commit -m "Updated image versions to ${BUILD_NUMBER}"'
            sh 'git push origin main'
        }
    }
}

        stage('Trigger Argo CD Deployment') {
            steps {
                script {
                    sh """
                    argocd app sync frontend-app --wait --loglevel debug
                    argocd app sync backend-app --wait --loglevel debug
                    """
                }
            }
        }
    }
}
