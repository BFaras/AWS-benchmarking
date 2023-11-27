import boto3
import matplotlib.pyplot as plt
from datetime import timedelta
from credentials import aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region

def establish_cloudwatch_session():
    """Establish and return a CloudWatch session."""
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=aws_region
    )
    return session.client('cloudwatch')

# Load ELB ARN and Target Group ARNs from files
with open('lb_arn.txt', 'r') as f:
    elb_arn = f.read().strip()
    elb_arn = f"app/loadBalancerOne/{elb_arn[85:]}"

with open('target_group_arns.txt', 'r') as f:
    lines = f.readlines()
    target_grp_m_arn = f"targetgroup/target-group-cluster1/{lines[0].strip()[86:]}"
    target_grp_t_arn = f"targetgroup/target-group-cluster2/{lines[1].strip()[86:]}"

def fetch_metrics(cloudwatch, metric_name, stat, dimension, start_time, end_time):
    """Fetch metrics from CloudWatch."""
    print(f"Fetching {metric_name} metric data... \n")
    try:
        response = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "metric_query",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/ApplicationELB",
                            "MetricName": metric_name,
                            "Dimensions": dimension
                        },
                        "Period": 1,
                        "Stat": stat
                    }
                }
            ],
            StartTime=start_time - timedelta(minutes=3),
            EndTime= end_time + timedelta(minutes=20)
        )

        return response
    except Exception as e:
        print(f"Error fetching metric data: {e}")
        return 0

def generate_plot(metric_title, dimension_value, x_values, y_values):
    """Generate a plot for the given metric data."""
    print(f"Generating plot for {metric_title}... \n")
    try:
        fig, ax = plt.subplots()
        ax.set_title(f'Metric: {metric_title} for {dimension_value}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Metric Value')
        ax.grid()
        ax.plot(x_values, y_values, '-o')
        fig.savefig(f'figs/{metric_title.replace(" ", "_").replace(":", "").replace("(", "").replace(")", "")}.png')
        plt.close(fig)
        print(f"Plot generated: figs/{metric_title.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')}.png" + "\n")
    except Exception as e:
        print(f"Error generating plot: {e}")

def analytics(start_time, end_time):
    """Fetch and visualize the analytics metrics."""
    cloudwatch = establish_cloudwatch_session()
    
    dimensions = {
        "LoadBalancer": elb_arn,
        "TargetGroup_t": target_grp_t_arn,
        "TargetGroup_m": target_grp_m_arn
    }
    metrics_to_fetch = [
        {
            "title": "RequestCount (Sum): ",
            "metric_name": "RequestCount",
            "stat": "Sum",
            "dimension": [
                {
                    "Name": "LoadBalancer",
                    "Value": dimensions["LoadBalancer"]
                }
            ]
        },
        {
            "title": "RequestCount (Average): ",
            "metric_name": "RequestCount",
            "stat": "Average",
            "dimension": [
                {
                    "Name": "LoadBalancer",
                    "Value": dimensions["LoadBalancer"]
                }
            ]
        },
        
        {
            "title": "RequestCountPerTarget c1 (Average): ",
            "metric_name": "RequestCountPerTarget",
            "stat": "Average",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_m"]
                },
            ]
        },
        {
            "title": "RequestCountPerTarget c1 (Sum): ",
            "metric_name": "RequestCountPerTarget",
            "stat": "Sum",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_m"]
                },
            ]
        },
        
        {
            "title": "RequestCountPerTarget c2 (Average): ",
            "metric_name": "RequestCountPerTarget",
            "stat": "Average",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_t"]
                },
            ]
        },
        {
            "title": "RequestCountPerTarget c2 (Sum): ",
            "metric_name": "RequestCountPerTarget",
            "stat": "Sum",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_t"]
                },
            ]
        },

        {
            "title": "RequestCountPerTarget c2 (Sum): ",
            "metric_name": "RequestCountPerTarget",
            "stat": "Sum",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_t"]
                },
            ]
        },
        {
            "title": "TargetResponseTime c2 (Average): ",
            "metric_name": "TargetResponseTime",
            "stat": "Average",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_t"]
                },
                {
                    "Name": "LoadBalancer",
                    "Value": dimensions["LoadBalancer"]
                }
            ]
        },        
        {
            "title": "TargetResponseTime c1 (Average): ",
            "metric_name": "TargetResponseTime",
            "stat": "Average",
            "dimension": [
                {
                    "Name": "TargetGroup",
                    "Value": dimensions["TargetGroup_m"]
                },
                {
                    "Name": "LoadBalancer",
                    "Value": dimensions["LoadBalancer"]
                },
            ]
        },

    ]

    for metric in metrics_to_fetch:
        metric_name = metric["metric_name"]
        stat = metric["stat"]
        dimension_value = metric["dimension"][0]["Value"]
        dimension = metric["dimension"]

        values = fetch_metrics(cloudwatch, metric_name, stat,dimension , start_time, end_time)

        x_values = values['MetricDataResults'][0]['Timestamps'] #
        y_values = values['MetricDataResults'][0]["Values"]  #
        generate_plot(metric["title"], dimension_value, x_values, y_values)


