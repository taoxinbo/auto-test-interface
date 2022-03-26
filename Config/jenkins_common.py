import os
from datetime import datetime

import jenkins

# 定义远程的jenkins master server的url，以及port

jenkins_server_url = 'http://10.60.48.154:8080'

# 定义用户的User Id 和 API Token，获取方式同上文

user_id = 'taoxb'

api_token = 'taoxb'

# 构建job名为job_name的job（不带构建参数）

# res = server.build_job('yqs-普通接口自动化测试')
# print(f"打印res：{res}")
# String参数化构建job名为job_name的job, 参数param_dict为字典形式，如：param_dict= {"param1"：“value1”， “param2”：“value2”}
#
# server.build_job('yqs-普通接口自动化测试')
#
# # 获取job名为job_name的job的相关信息
#
# server.get_job_info('yqs-普通接口自动化测试')
#
# # 获取job名为job_name的job的最后次构建号
#
# name = server.get_job_info('yqs-普通接口自动化测试')['lastBuild']['number']
# print(name)
# # 获取job名为job_name的job的某次构建的执行结果状态
#
# server.get_build_info('yqs-普通接口自动化测试', name)['result']
#
# # 判断job名为job_name的job的某次构建是否还在构建中
#
# server.get_build_info('yqs-普通接口自动化测试', name)['building']
job_name = 'oracle_stopAll_interfaceauto'


class jenkins_operation:

    def __init__(self, user_id, api_token, job_name, jenkins_server_url):
        """
        :param jenkins_server_url: jenkins 地址+端口号
        :param user_id: 账号
        :param api_token: 密码
        :param job_name: 构建的项目名称
        """
        self.user_id = user_id
        self.api_token = api_token
        self.job_name = job_name
        self.jenkins_server_url = jenkins_server_url
        self.server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

    def get_job_all_list(self):
        """
        :return: 返回当前账号所有的job
        """
        Jobs = self.server.get_jobs()
        return Jobs

    def job_all_build_list(self):
        """
        :param job_name: job名称
        :return:当前job所有的构建记录
        """
        last_build_info = self.server.get_job_info(self.job_name)
        builds = last_build_info['builds']
        print(f"当前job所有的构建记录:{builds}")
        return builds

    def run_job(self):
        if self.job_name in [i['name'] for i in self.server.get_all_jobs()]:
            res = self.server.build_job(self.job_name)
            print(f"构建完成，构建的编号是：{res}")
            return f"构建完成，构建的编号是：{res}"
        else:
            print(f'{job_name}项目名称不存在')
            return f'{job_name}项目名称不存在'

    def get_jobs_status(self, job_name):
        """
        :param job_name: 传入指定的 任务名称
        :param server: 传入服务
        :return: 返回最新的执行总数，返回最新的job---id
        """
        try:
            self.server.assert_job_exists(job_name)
        except Exception as e:
            print(e)
            job_statue = '1'
        # 判断job是否处于排队状态
        inQueue = self.server.get_job_info(job_name)['inQueue']
        if str(inQueue) == 'True':
            job_statue = 'pending'
            running_number = self.server.get_job_info(job_name)['nextBuildNumber']
        else:
            # 先假设job处于running状态，则running_number = nextBuildNumber -1 ,执行中的job的nextBuildNumber已经更新
            running_number = self.server.get_job_info(job_name)['nextBuildNumber'] - 1
            try:
                running_status = self.server.get_build_info(job_name, running_number)['building']
                if str(running_status) == 'True':
                    job_statue = 'running'
                else:
                    # 若running_status不是True说明job执行完成
                    job_statue = self.server.get_build_info(job_name, running_number)['result']
            except Exception as e:
                # 上面假设job处于running状态的假设不成立，则job的最新number应该是['lastCompletedBuild']['number']
                lastCompletedBuild_number = self.server.get_job_info(job_name)['lastCompletedBuild']['number']
                job_statue = self.server.get_build_info(job_name, lastCompletedBuild_number)['result']
        return job_statue, running_number

    def get_build_state(self, name, build_number):
        """
        :param name: job_name
        :param build_number: 最后1次构建序号
        :param:jenkins_server
        :return: 最后1次构建状态 pending,success,false,building
        """
        build_state = None
        # 获取正在排队构建的job队列 即pending状态中的所有job,如果没有 pending状态的job即返回1个空列表
        queue_info = self.server.get_queue_info()
        if queue_info:
            for queue_job_info in queue_info:
                if queue_job_info['task']['name'] == name:
                    # msg = 'pending期,排队构建中'
                    build_state = 'pending'
        else:

            build_state = self.server.get_build_info(name, build_number)['result']
        # 构建结束 SUCCESS|FAILURE<class 'str'>   ABORTED:终止 <class 'str'>  构建中None  None <class 'NoneType'>
        return build_state

    # 停止build
    def stop(self, job_id):
        if job_id in self.server.get_all_jobs():
            if job_id in self.server.get_queue_info()['task']['name']:
                self.server.stop_build(self.job_name, job_id)
            else:
                pass

    def jenkins_log(self, job_name, job_id):
        """
        :param job_name: job名称
        :param job_id: job id
        :return: 当前id构建的日志信息
        """
        server = jenkins.Jenkins(self.jenkins_server_url, username=self.user_id, password=self.api_token)
        job_log = server.get_build_console_output(job_name, job_id)
        print(job_log)


if __name__ == '__main__':
    pass
