pipeline {
    agent any

    environment {
        FRONTEND_IMAGE = 'itsmesimha/frontend-nginx'
        BACKEND_IMAGE = 'itsmesimha/backend-flask'
        IMAGE_TAG = "${BUILD_NUMBER}"
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
                        docker build -t $FRONTEND_IMAGE:$IMAGE_TAG frontend/
                        docker build -t $BACKEND_IMAGE:$IMAGE_TAG backend/
                        
                        echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin
                        docker push $FRONTEND_IMAGE:$IMAGE_TAG
                        docker push $BACKEND_IMAGE:$IMAGE_TAG
                        docker logout
                        """
                    }
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    sh """
                    sed -i 's|image: itsmesimha/frontend-nginx:.*|image: itsmesimha/frontend-nginx:${IMAGE_TAG}|' manifest/frontend/deployment.yaml
                    sed -i 's|image: itsmesimha/backend-flask:.*|image: itsmesimha/backend-flask:${IMAGE_TAG}|' manifest/backend/deployment.yaml
                    """
                    
                    withCredentials([usernamePassword(credentialsId: 'gitHub-credentials', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                        sh """
                        git config --global user.email "hongirana.s@cloudjournee.com"
                        git config --global user.name "itsmesimha"
                        git add manifest/frontend/deployment.yaml manifest/backend/deployment.yaml
                        git commit -m "Updated image versions to ${IMAGE_TAG}"
                        git push https://$GITHUB_USER:$GITHUB_TOKEN@github.com/itsmesimhaa/Dockerized-CICD.git main
                        """
                    }
                }
            }
        }

        stage('Trigger Argo CD Deployment') {
    steps {
        script {
            withCredentials([string(credentialsId: 'argocd-token', variable: 'ARGOCD_AUTH_TOKEN')]) {
                sh """
                argocd login 13.59.209.207:30285 --auth-token=$ARGOCD_AUTH_TOKEN --insecure
                argocd app sync frontend-app --sync-wait --loglevel debug
                argocd app sync backend-app --sync-wait --loglevel debug
                """
            }
        }
    }
}
