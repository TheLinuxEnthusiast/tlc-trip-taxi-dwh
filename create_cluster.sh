#!/bin/bash
# Author: Darren Foley
# Email: darren.foley@ucdconnect.ie
# Description: Creates a new redshift cluster for production or for testing
#####################################################

DEFAULT_NAME="redshift-cluster-test-1"
DEFAULT_TYPE="single-node"
DEFAULT_SG="sg-12d2990e"
DEFAULT_REGION="us-east-1"
DEFAULT_USER="awsuser"
DEFAULT_PW="KalmPanik91!"
DEFAULT_NODE_SIZE="dc2.large"
DEFAULT_PROFILE="admin"
DEFAULT_NUMBER_OF_NODES=1
PROD_NAME="tlc-production-dwh"
PROD_NODE_SIZE="ra3.xlplus"
PROD_NUMBER_OF_NODES=3
PROD_TYPE="multi-node"

ISTEST=

usage(){
	echo "$0 [-T|testing] [-P|production] [-d|delete] <cluster-identifier>"
	exit 1
}

while getopts "TPd:" opt
do
	case "$opt" in
	T)
		ISTEST=0
	;;
	P)
		ISTEST=1
	;;
	d)
		CLUSTER_NAME="${OPTARG}"
	;;
    h)
        usage
    ;;
	*)
		usage
	;;
	esac
done
shift $((OPTIND-1))

#if [ -z "${CLUSTER_NAME}" ] & [ -z "${ISTEST}" ]; then
#	usage
#fi

create_cluster(){
	
	if [ "${ISTEST}" = "0" ];
    then

		aws redshift create-cluster \
			--cluster-identifier ${DEFAULT_NAME} \
			--master-username ${DEFAULT_USER} \
			--master-user-password ${DEFAULT_PW} \
			--node-type ${DEFAULT_NODE_SIZE} \
            --number-of-nodes ${DEFAULT_NUMBER_OF_NODES} \
			--cluster-type ${DEFAULT_TYPE} \
			--publicly-accessible \
			--profile ${DEFAULT_PROFILE}
	else
		aws redshift create-cluster \
                        --cluster-identifier ${PROD_NAME} \
                        --master-username ${DEFAULT_USER} \
                        --master-user-password ${DEFAULT_PW} \
                        --node-type ${PROD_NODE_SIZE} \
                        --number-of-nodes ${PROD_NUMBER_OF_NODES} \
                        --cluster-type ${PROD_TYPE} \
                        --publicly-accessible \
                        --profile ${DEFAULT_PROFILE}

	fi


}
#create_cluster

delete_cluster(){
	
	aws redshift delete-cluster \
			--cluster-identifier ${CLUSTER_NAME} \
			--skip-final-cluster-snapshot \
			--profile ${DEFAULT_PROFILE}
}
#delete_cluster

main(){

	if [ ! -z "${CLUSTER_NAME}" ]; 
    then
		echo "deleting cluster....."
		delete_cluster
		exit 0
	else
		echo "creating cluster......"
		create_cluster
	fi

}
main
