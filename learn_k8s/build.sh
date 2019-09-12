#!/usr/bin/env bash
re="100.125.17.64:20202/lanjing/([^:]+):([^ ]+)"
imageStr=$(kubectl --kubeconfig $KTHWTEST get deploy paw-spider-store -o jsonpath='{..image}')
echo "current version"
if [[ $imageStr =~ $re ]]; then echo ${BASH_REMATCH[2]}; fi


if [ $# -eq 0 ];
then nextVersion=$(./increment_version.sh -p ${BASH_REMATCH[2]});
else nextVersion=$(./increment_version.sh $1 ${BASH_REMATCH[2]});
fi

echo "next version"
echo $nextVersion;

# git add .
# git commit -m $nextVersion --no-verify
# git push

docker build -t swr.cn-east-2.myhuaweicloud.com/lanjing/paw-spider-store:$nextVersion .
docker push swr.cn-east-2.myhuaweicloud.com/lanjing/paw-spider-store:$nextVersion

kubectl --kubeconfig $KTHWTEST set image deployment/swr.cn-east-2.myhuaweicloud.com/lanjing/paw-spider-store:$nextVersion
kubectl --kubeconfig $KTHWTEST get pod -l app=paw-spider-store
