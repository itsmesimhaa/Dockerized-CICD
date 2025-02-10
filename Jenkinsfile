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
                        git add manifest/frontend/deployment.yaml manifest/backend/deployment.yaml manifest/frontend/nginx-configmap.yaml
                        git commit -m "Updated image versions to ${IMAGE_TAG} and ConfigMap"
                        git push https://$GITHUB_USER:$GITHUB_TOKEN@github.com/itsmesimhaa/Dockerized-CICD.git main
                        """
                    }
                }
            }
        }

                stage('Trigger Argo CD Deployment') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'argocd-credentials', usernameVariable: 'ARGOCD_USER', passwordVariable: 'ARGOCD_PASSWORD')]) {
                        sh """
                        argocd login 3.128.199.148:31191 --username='$ARGOCD_USER' --password='$ARGOCD_PASSWORD' --insecure
                        
                        # Wait for any ongoing sync operation to complete
                        while argocd app get frontend | grep -q 'Sync: Running'; do
                            echo "Waiting for existing sync operation to complete..."
                            sleep 10
                        done

                        # Trigger ArgoCD sync for frontend
                        argocd app sync frontend --loglevel debug || echo "ArgoCD sync failed, retrying in 10 seconds" && sleep 10 && argocd app sync frontend --loglevel debug

                        # Wait again to ensure the operation completes before proceeding
                        while argocd app get backend | grep -q 'Sync: Running'; do
                            echo "Waiting for existing sync operation to complete..."
                            sleep 10
                        done

                        # Trigger ArgoCD sync for backend
                        argocd app sync backend --loglevel debug || echo "ArgoCD sync failed, retrying in 10 seconds" && sleep 10 && argocd app sync backend --loglevel debug
                        """
                    }
                }
            }
        }

