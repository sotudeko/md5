
pipeline {
    agent any

    environment {
        DEV_REPO = 'raw-releases'
        TAG_FILE = "${WORKSPACE}/tag.json"
        IQ_SCAN_URL = ""
				ARTEFACT_NAME="md5"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'mkdir build'
            }
            post {
                success {
                    echo 'Now installing dependencies...'
                    sh 'cd build && conan install ..'

                }
            }
        }

		stage('Build') {
				steps {
					dir("./build"){
						sh 'cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release'
					}
				}
				post {
					success {
						dir("./build"){
							sh 'cmake --build .'
						}
					}
				}
		}
				
		stage('Test'){
				steps {
					dir("./build"){
						sh './bin/md5'
					}
				}
		}

        stage('Nexus IQ Scan'){
            steps {
                script{
                    sh 'ansible-playbook /Users/sotudeko/Development/mygithub/nx-ansible/playbooks/nxiq-scan.yml --extra-vars "application=md5app-ans target=conanfile.txt stage=build"'
                }
            }
        }

        stage('Create tag'){
            steps {
                script {
    
                    // Git data (Git plugin)
                    echo "${GIT_COMMIT}"
                    echo "${GIT_URL}"
                    echo "${GIT_BRANCH}"
                    echo "${WORKSPACE}"
                    
                    // construct the meta data (Pipeline Utility Steps plugin)
                    def tagdata = readJSON text: '{}' 
                    tagdata.buildUser = "${USER}" as String
                    tagdata.buildNumber = "${BUILD_NUMBER}" as String
                    tagdata.buildId = "${BUILD_ID}" as String
                    tagdata.buildJob = "${JOB_NAME}" as String
                    tagdata.buildTag = "${BUILD_TAG}" as String
                    tagdata.appVersion = "${BUILD_VERSION}" as String
                    tagdata.buildUrl = "${BUILD_URL}" as String
                    //tagdata.iqScanUrl = "${IQ_SCAN_URL}" as String
                    //tagData.promote = "no" as String

                    writeJSON(file: "${TAG_FILE}", json: tagdata, pretty: 4)

                    createTag nexusInstanceId: 'nxrm3', tagAttributesPath: "${TAG_FILE}", tagName: "${BUILD_TAG}"

                    // write the tag name to the build page (Rich Text Publisher plugin)
                    rtp abortedAsStable: false, failedAsStable: false, parserName: 'Confluence', stableText: "Nexus Repository Tag: ${BUILD_TAG}", unstableAsStable: true 
                }
            }
						post {
							success {
              	sh 'echo tag_file: && cat ${TAG_FILE}'
							}
						}
        }

        stage('Upload to Nexus Repository'){
            steps {
                script {
					sh 'curl -v -u admin:admin123 --upload-file ./build/bin/${ARTEFACT_NAME} http://localhost:8081/repository/${DEV_REPO}/${ARTEFACT_NAME}/${BUILD_VERSION}/${ARTEFACT_NAME}'
                }
            }
        }
    }
}

