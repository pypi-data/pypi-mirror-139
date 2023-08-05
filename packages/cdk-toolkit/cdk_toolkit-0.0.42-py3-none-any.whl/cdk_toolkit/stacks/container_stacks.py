from aws_cdk import Stack 
from constructs import Construct
import aws_cdk

from cdk_toolkit import connection, container, permission


class EKSStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, eks_cluster_name: str, eks_role_arn: str, vpc: connection.ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_role =  permission.iam.Role.from_role_arn(self, "eks_admin_role", role_arn=eks_role_arn)
        eks_instance_profile = permission.createIAMInstanceProfile(self, "eks-instance-profile", eks_role) 
        
        # EC2 EKS
        # cluster = container.createEKS_EC2Cluster(self, eks_cluster_name, eks_role, vpc)
        # nodegroup = container.addEKS_EC2ClusterNodeGroup(self, cluster) 

        # FARGATE EKS
        fargate = container.createEKS_FargateCluster(self, eks_cluster_name, eks_role, vpc)


class EMR_EKSStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, cluster: container.eks.FargateCluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.emr_namespace = "sparkns"
        self.emr_namespace_fg = "sparkfg"
        self.emrsvcrolearn = f"arn:aws:iam::{self.account}:role/AWSServiceRoleForAmazonEMRContainers"
        self.instance_type = self.node.try_get_context("instance")



        # Create namespaces for EMR to use
        namespace = self.cluster.add_manifest(self.emr_namespace, {
            "apiVersion":"v1",
            "kind":"Namespace",
            "metadata":{"name": self.emr_namespace},
        })
        namespace_fg = self.cluster.add_manifest(self.emr_namespace_fg, {
            "apiVersion":"v1",
            "kind":"Namespace",
            "metadata":{"name": self.emr_namespace_fg},
        })

        # Fargate profile
        fgprofile = container.eks.FargateProfile(self, "SparkFargateProfile", cluster=self.cluster, 
            selectors=[{"namespace": self.emr_namespace_fg}]
        )

        # Create k8s cluster role for EMR
        emrrole = self.cluster.add_manifest("emrrole", {
            "apiVersion":"rbac.authorization.k8s.io/v1",
            "kind":"Role",
            "metadata":{"name": "emr-containers", "namespace": self.emr_namespace},
            "rules": [
                {"apiGroups": [""], "resources":["namespaces"],"verbs":["get"]},
                {"apiGroups": [""], "resources":["serviceaccounts", "services", "configmaps", "events", "pods", "pods/log"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "deletecollection", "annotate", "patch", "label"]},
                {"apiGroups": [""], "resources":["secrets"],"verbs":["create", "patch", "delete", "watch"]},
                {"apiGroups": ["apps"], "resources":["statefulsets", "deployments"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["batch"], "resources":["jobs"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["extensions"], "resources":["ingresses"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["rbac.authorization.k8s.io"], "resources":["roles", "rolebindings"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "deletecollection", "annotate", "patch", "label"]}
            ]
        })
        emrrole.node.add_dependency(namespace)
        emrrole_fg = self.cluster.add_manifest("emrrole_fg", {
            "apiVersion":"rbac.authorization.k8s.io/v1",
            "kind":"Role",
            "metadata":{"name": "emr-containers", "namespace": self.emr_namespace_fg},
            "rules": [
                {"apiGroups": [""], "resources":["namespaces"],"verbs":["get"]},
                {"apiGroups": [""], "resources":["serviceaccounts", "services", "configmaps", "events", "pods", "pods/log"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "deletecollection", "annotate", "patch", "label"]},
                {"apiGroups": [""], "resources":["secrets"],"verbs":["create", "patch", "delete", "watch"]},
                {"apiGroups": ["apps"], "resources":["statefulsets", "deployments"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["batch"], "resources":["jobs"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["extensions"], "resources":["ingresses"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "annotate", "patch", "label"]},
                {"apiGroups": ["rbac.authorization.k8s.io"], "resources":["roles", "rolebindings"],"verbs":["get", "list", "watch", "describe", "create", "edit", "delete", "deletecollection", "annotate", "patch", "label"]}
            ]
        })
        emrrole_fg.node.add_dependency(namespace_fg)

        # Bind cluster role to user
        emrrolebind = self.cluster.add_manifest("emrrolebind", {
            "apiVersion":"rbac.authorization.k8s.io/v1",
            "kind":"RoleBinding",
            "metadata":{"name": "emr-containers", "namespace": self.emr_namespace},
            "subjects":[{"kind": "User","name":"emr-containers","apiGroup": "rbac.authorization.k8s.io"}],
            "roleRef":{"kind":"Role","name":"emr-containers","apiGroup": "rbac.authorization.k8s.io"}
        })
        emrrolebind.node.add_dependency(emrrole)
        emrrolebind_fg = self.cluster.add_manifest("emrrolebind_fg", {
            "apiVersion":"rbac.authorization.k8s.io/v1",
            "kind":"RoleBinding",
            "metadata":{"name": "emr-containers", "namespace": self.emr_namespace_fg},
            "subjects":[{"kind": "User","name":"emr-containers","apiGroup": "rbac.authorization.k8s.io"}],
            "roleRef":{"kind":"Role","name":"emr-containers","apiGroup": "rbac.authorization.k8s.io"}
        })
        emrrolebind_fg.node.add_dependency(emrrole_fg)

        # Map user to IAM role
        emrsvcrole = permission.iam.Role.from_role_arn(self, "EmrSvcRole", self.emrsvcrolearn, mutable=False)
        self.cluster.aws_auth.add_role_mapping(emrsvcrole, groups=[], username="emr-containers")

         # Job execution role
        self.job_role = permission.iam.Role(self, "EMR_EKS_Job_Role", assumed_by=permission.iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                permission.iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                permission.iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
                permission.iam.ManagedPolicy.from_aws_managed_policy_name("AWSGlueConsoleFullAccess"),
                permission.iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")])
        aws_cdk.CfnOutput(
            self, "JobRoleArn",
            value=self.job_role.role_arn
        )