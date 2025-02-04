pipeline {
    agent any
    
    environment {
        FRONTEND_IMAGE = 'itsmesimha/frontend-nginx'
        BACKEND_IMAGE = 'itsmesimha/backend-flask'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/itsmesimhaa/END-TO-END-CICD-PIPELINE-OF-THREE-TIER-ARCHITECTURE'
            }
        }
        
        stage('Build and Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Docker-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                    script {
                        sh 'docker build -t $FRONTEND_IMAGE:latest frontend/'
                        sh 'docker build -t $BACKEND_IMAGE:latest backend/'

                        sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin'
                        sh 'docker push $FRONTEND_IMAGE:latest'
                        sh 'docker push $BACKEND_IMAGE:latest'
                        sh 'docker logout'
                    }
                }
            }
        }
        
        stage('Trigger Argo CD Deployment') {
            steps {
                script {
                    sh 'argocd app sync frontend-app --wait'
                    sh 'argocd app sync backend-app --wait'
                }
            }
        }
    }
}
