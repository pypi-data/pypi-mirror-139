#-*- coding:utf8 -*-
'''
Created on 2021年7月26日

@author: mrray
'''

import configparser
import time
from seleniumWebUi.USelenium import USelenium
from config import setting


class raybaas_function():
    def __init__(self, down_dir=None, driver='chrome', options=None):
        self.drive = USelenium()
        self.config_params()
        self.drive.initDriver(driverType=driver, downDir=down_dir, options=options)
        
    
    def config_params(self):
        config = configparser.ConfigParser()
        config.read(setting.TEST_CONFIG, encoding='utf-8')
        self.ip     =   config.get('url', 'ip')
        self.port   =   config.get('url', 'port')
        self.s_url  =   config.get('url', 'server_url')
        self.c_url  =   config.get('url', 'client_url')
        self.s_user =   config.get('account', 'server_user')
        self.c_user =   config.get('account', 'client_user')
        self.s_pass =   config.get('account', 'server_pass')
        self.c_pass =   config.get('account', 'client_pass')
    
    
    def open_url(self, url):
        '''
        打开登录页
        :param url:
        '''
        login_url = 'http://' + self.ip + url
        try:
            self.drive.openUrl(login_url)
            return True
        except Exception as e:
            return e
        
        
    def login(self, login_type, username, password):
        '''
        用户登录---区分管理端和用户端
        :param login_type:
        :param username:
        :param password:
        :param name_xpath:
        :param pass_xpath:
        :param button_xpath:
        '''
       
#         '//*[@id="adminLogin"]/div/div[1]/input', '//*[@id="adminLogin"]/div/div[2]/input', '//*[@id="adminLogin"]/div/button')
        
        # 登录操作
        try:
            # 登录界面打开
            if(login_type.lower() == 'admin'):
                page_re = self.open_url(self.s_url)
                time.sleep(5)
                self.drive.setText('xpath', '//*[@id="adminLogin"]/div/div[1]/input', username)
                time.sleep(1)
                self.drive.setText('xpath', '//*[@id="adminLogin"]/div/div[2]/input', password)
                time.sleep(1)
                self.drive.click('xpath', '/html/body/div/section/section/div[1]/div/button')
            elif (login_type.lower() == 'user'):
                page_re = self.open_url(self.c_url)
                time.sleep(5)
                self.drive.setText('xpath', '//*[@id="login"]/div/div[1]/input', username)
                time.sleep(1)
                self.drive.setText('xpath', '//*[@id="login"]/div/div[2]/input', password)
                time.sleep(1)
                self.drive.click('xpath', '//*[@id="login"]/div/button')
            if page_re!=True:
                return page_re
            
        except Exception as e:
            return e
        return True
    
    
    def logout(self):
        '''
        用户登出
        '''
        # 登录界面打开
        self.drive.mouseOver('xpath', '/html/body/div[1]/section/header/header/span[3]/div/span')
        time.sleep(3)
        self.drive.click('xpath', '/html/body/ul/li[2]')
        time.sleep(3)                  
        self.drive.click('xpath', '/html/body/div[2]/div/div[3]/button[2]')
        
    
    def table_len(self, table_xpath):
        '''
        判断列表长度
        :param table_xpath:
        '''
        exist = True
        count = 0
        while exist:
            exist = self.drive.elementIsExist('xpath', table_xpath+'/tr['+str(count+1)+']')
            if exist:
                count = count + 1
        
        time.sleep(3)
        return count
    
    
    def user_exist(self, username):
        '''
        判断用户是否存在
        :param username:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入用户管理
        isExist = None
        self.drive.click('xpath', '/html/body/div[1]/section/section/aside/ul/li[5]/div')
        time.sleep(1)
        
        # 获取用户列表
        rows = self.table_len('//*[@id="user"]/div[2]/div[1]/div[3]/table/tbody')
        for i in range(1, rows+1):
            user = self.drive.getText('xpath', '//*[@id="user"]/div[2]/div[1]/div[3]/table/tbody/tr['+str(i)+']/td[2]/div')
            if user == username:
                isExist = user
        return isExist
        
    
    def add_user(self, username, password, email, role):
        '''
        添加用户
        :param username:
        :param password:
        :param email:
        :param role:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入用户管理
        self.drive.click('xpath', '/html/body/div[1]/section/section/aside/ul/li[5]/div/span')
        
        # 新增用户并填写用户信息
        self.drive.click('xpath', '//*[@id="user"]/div[1]/button[1]')
        self.drive.setText('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[1]/div/div/input', username)
        self.drive.setText('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[2]/div/div/input', password)
        self.drive.setText('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[3]/div/div/input', password)
        self.drive.setText('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[4]/div/div/input', email)
        
        # 选择权限
        if role.lower() == "user":
            self.drive.click('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[5]/div/div/label[1]/span[1]/span')
        elif role.lower() == "admin":
            self.drive.click('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[1]/form/div[5]/div/div/label[2]/span[1]/span')
        
        # 点击确认按钮
        self.drive.click('xpath', '//*[@id="user"]/div[2]/div[4]/div/div[2]/div[2]/button[1]')
        
        
    
    def add_server(self, servername, ip, port, username, passwd):
        '''
        添加服务器
        :param servername:
        :param ip:
        :param port:
        :param username:
        :param passwd:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入服务器管理界面
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/span')
        
        # 点击新增并填写服务器信息
        self.drive.click('xpath', '//*[@id="resourcePoint"]/div[1]/button')
        self.drive.setText('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[1]/form/div[1]/div/div/input', servername)
        self.drive.setText('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[1]/form/div[2]/div/div/input', ip)
        self.drive.setText('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[1]/form/div[3]/div/div/input', port)
        self.drive.setText('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[1]/form/div[4]/div/div/input', username)
        self.drive.setText('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[1]/form/div[5]/div/div/input', passwd)
        
        # 点击确认按钮
        self.drive.click('xpath', '//*[@id="resourcePoint"]/div[4]/div/div[2]/div/div[2]/button[1]')
        time.sleep(3)
        
    
    def server_del(self, ip):
        '''
        删除服务器
        :param ip:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入服务器管理
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/span')
        time.sleep(1)
        
        # 获取服务器列表
        rows = self.table_len('//*[@id="resourcePoint"]/div[2]/div/div[3]/table/tbody')
        for i in range(1, rows+1):
            server = self.drive.getText('xpath', '//*[@id="resourcePoint"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[4]/div')
            if server == ip:
                # 删除服务器
                self.drive.click('xpath', '//*[@id="resourcePoint"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[7]/div/span[2]')
                
                time.sleep(3)
                # 确定删除
                self.drive.click('css', 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary')

                
        
    def server_exist(self, ip):
        '''
        判断用户是否存在
        :param username:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入服务器管理
        isExist = None
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/span')
        time.sleep(1)
        
        # 获取服务器列表
        rows = self.table_len('//*[@id="resourcePoint"]/div[2]/div/div[3]/table/tbody')
        for i in range(1, rows+1):
            server = self.drive.getText('xpath', '//*[@id="resourcePoint"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[4]/div')
            if server == ip:
                isExist = server
        return isExist
    
    
    def order_apply(self, order_class, text_value, file_path):
        '''
        创建工单任务
        :param order_class:
        :param text_value:
        :param file_path:
        '''
        self.drive.refresh()
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入工单
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[5]')
        
        # 点击提交工单
        self.drive.click('xpath', '//*[@id="order"]/div[1]/button[2]')
        
        # 选择工单分类
        i=1
        while True:
            i = i + 1
            if self.drive.click('xpath', '//*[@id="order"]/div[3]/div['+str(i)+']/div/div[2]/div[1]/form/div[1]/div/div/div/span') == True:
                break
                                    
        time.sleep(3)
        for j in range(1,7):
            if self.drive.getText('css', 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child('+str(j)+') > span') == order_class:
                self.drive.click('css', 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child('+str(j)+') > span')
                break
            
        # 填写工单描述
        self.drive.setText('xpath', '//*[@id="order"]/div[3]/div['+str(i)+']/div/div[2]/div[1]/form/div[2]/div/div[1]/textarea', text_value)
        
        # 上传文件
        self.drive.upload_file('xpath', '//*[@id="order"]/div[3]/div['+str(i)+']/div/div[2]/div[1]/form/div[3]/div/div/div/button', file_path)
        
        time.sleep(3)
        self.drive.click('xpath', '//*[@id="order"]/div[3]/div['+str(i)+']/div/div[2]/div[2]/button[1]')
        
    
    def chain_applay(self, name, peer, order, common_mode):
        '''
        创建区块链
        :param name:
        :param peer:
        :param order:
        :param common_mode:
        '''
        self.drive.refresh()
        time.sleep(2)
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入区块链申请
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/div/span')
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/ul/li[1]')
        time.sleep(2)
        
        # 申请区块链
        self.drive.click('xpath', '//*[@id="blockManage"]/div[1]/button')
        time.sleep(2)
        # 填写区块链名称和选择共识方式
        self.drive.setText('xpath', '//*[@id="blockManage"]/div[3]/div/div[2]/div/section/div[1]/form/div[1]/div/div[1]/input', name)
        self.drive.click('xpath', '/html/body/div[1]/section/section/main/section/div[1]/div[3]/div/div[2]/div/section/div[1]/form/div[2]/div/div/div/input')
        time.sleep(2)
        # 判断申请共识方式
        mode = 1
        if common_mode == 'pbft':
            mode = 2
        elif common_mode == 'raft':
            mode = 3
        elif common_mode == 'kafka':
            mode = 1
        else:
            print("共识方式填写错误！")
            return False
        self.drive.click('css', 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child('+str(mode)+')')
        # 填写共识和记帐节点数量
        self.drive.setText('xpath', '//*[@id="blockManage"]/div[3]/div/div[2]/div/section/div[2]/form/div[1]/div/div/div/input', str(peer))
        self.drive.setText('xpath', '/html/body/div[1]/section/section/main/section/div[1]/div[3]/div/div[2]/div/section/div[2]/form/div[2]/div/div/div/input', str(order))
        time.sleep(2)
        
        # 提交申请
        self.drive.click('xpath', '//*[@id="blockManage"]/div[3]/div/div[2]/div/div/button[1]')
        time.sleep(3)
        
    
    def chain_del(self, chain_name):
        '''
        删除区块链
        :param chain_name:
        '''
        self.drive.refresh()
        time.sleep(3)
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入区块链申请
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/div/span')
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/ul/li[1]')
        time.sleep(3)
        
        # 获取区块链列表
        rows = self.table_len('//*[@id="blockManage"]/div[2]/div/div[3]/table/tbody')
        
        for i in range(1, rows+1):
            get_name = self.drive.getText('xpath', '/html/body/div/section/section/main/section/div[1]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[3]/div')
            if get_name == chain_name:
                # 删除区块链
                self.drive.click('xpath', '/html/body/div/section/section/main/section/div[1]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[8]/div/span[3]')
                time.sleep(2)
                # 确定删除
                self.drive.click('css', 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary')
                time.sleep(2)
                
    def chain_audit(self, chain_name):
        '''
        审核区块链
        :param chain_name:
        '''
        self.drive.refresh()
        time.sleep(3)
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入区块链申请管理
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[3]/div')
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[3]/ul/li[1]')
        time.sleep(3)
        
        # 获取区块链列表
        rows = self.table_len('//*[@id="resourceWeb"]/div[3]/div/div[3]/table/tbody')
        
        for i in range(1, rows+1):
            get_name = self.drive.getText('xpath', '//*[@id="resourceWeb"]/div[3]/div/div[3]/table/tbody/tr['+str(i)+']/td[5]/div')
            if get_name == chain_name:
                # 审核区块链
                self.drive.click('xpath', '//*[@id="resourceWeb"]/div[3]/div/div[3]/table/tbody/tr['+str(i)+']/td[9]/div/span')
                time.sleep(2)
                # 确定审核
                self.drive.click('css', '#resourceWeb > div:nth-child(6) > div > div.el-dialog__body > div > div.footer > button')
                time.sleep(2)
                # 稍后部署
                self.drive.click('css', 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button:nth-child(1)')
                time.sleep(2)
    
    
    def chain_deploy(self, chain_name):
        '''
        部署区块链
        :param chain_name:
        '''
        self.drive.refresh()
        time.sleep(3)
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入区块链网络管理-待部署
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[3]/div')
        self.drive.click('xpath', '/html/body/div[1]/section/section/aside/ul/li[3]/ul/li[2]')
        self.drive.click('xpath', '/html/body/div[1]/section/section/main/section/div[1]/div[1]/div[2]')
        time.sleep(3)
        
        # 获取区块链列表
        rows = self.table_len('//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody')
        list_num = 0
        for i in range(1, rows+1):
            get_name = self.drive.getText('xpath', '//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[2]/div')
            if get_name == chain_name:
                list_num = i
                break
            
        # 部署区块链
        self.drive.click('xpath', '//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody/tr['+str(list_num)+']/td[9]/div/span')
        time.sleep(2)
        
        # 获取节点列表
        row_nodes = self.table_len('//*[@id="content"]/section/div[1]/div/div[3]/table/tbody')
        print(row_nodes)
        for i in range(1, row_nodes+1):
            self.drive.click('xpath', '//*[@id="content"]/section/div[1]/div/div[3]/table/tbody/tr['+str(i)+']/td[5]/div/span')
            time.sleep(1)
            self.drive.click('xpath', '//*[@id="content"]/div[1]/div/div[2]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
            time.sleep(3)  
            # 自动获取端口 
            self.drive.click('xpath', '//*[@id="content"]/div[1]/div/div[2]/div/div[1]/p[2]/span')
            time.sleep(3)
            self.drive.click('xpath', '//*[@id="content"]/div[1]/div/div[2]/div/div[2]/button[1]')
            time.sleep(3)  
                                     
        # 确定部署
        self.drive.click('xpath', '//*[@id="resourceDetails"]/p[2]/button[1]')
        time.sleep(2)
        
        element_exist = False
        while not element_exist:
            element_exist = self.drive.elementIsExist('xpath', '//*[@id="step6"]/div[4]/button')
            time.sleep(1)
        
        # 点击完成
        self.drive.click('xpath', '//*[@id="step6"]/div[4]/button')
        time.sleep(2)
        
        # 判断区块链是否运行
        rows = self.table_len('//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody')
        chain_status = None
        count = 0
        for i in range(1, rows+1):
            get_name = self.drive.getText('xpath', '//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[2]/div')
            if get_name == chain_name:
                chain_status = self.drive.getText('xpath', '//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[8]/div/span')
                while chain_status!="运行中":
                    self.drive.refresh()
                    chain_status = self.drive.getText('xpath', '//*[@id="resourceWeb2"]/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[8]/div/span')
                    count = count + 1
                    if count >= 1000:
                        return False
                    time.sleep(5)
        
                return True
    
    
    def chain_peer_num(self, chain_name):
        self.drive.refresh()
        time.sleep(3)
        
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[1]')
        time.sleep(1)
        
        # 进入区块链申请
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/div/span')
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[2]/ul/li[2]')
        time.sleep(2)
        
        # 获取区块链列表
        rows = self.table_len('//*[@id="blockManage"]/div[3]/div[1]/div[3]/table/tbody')
        list_num = 0
        for i in range(1, rows+1):
            get_name = self.drive.getText('xpath', '//*[@id="blockManage"]/div[3]/div[1]/div[3]/table/tbody/tr['+str(i)+']/td[2]/div')
            print(get_name)
            if get_name == chain_name:
                list_num = i
                break
            
        time.sleep(1)
        self.drive.click('xpath', '//*[@id="blockManage"]/div[3]/div[1]/div[3]/table/tbody/tr['+str(list_num)+']/td[9]/div/span[1]')
        time.sleep(1)
        self.drive.click('xpath', '//*[@id="tab-/BlockManage/BlockData"]')
        peer_num = self.drive.getText('xpath', '/html/body/div[1]/section/section/main/section/div[1]/div/div[2]/div/div/div[10]')
        print('peer_num: ', peer_num)
        time.sleep(10)
        return peer_num
            
    
    def order_download_attach(self):
        self.drive.refresh()
        
        # 进入管理端工单 
        self.drive.click('xpath', '//*[@id="asideBox"]/ul/li[6]')
        
        self.drive.click('xpath', '//*[@id="order"]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[8]/div/span')

        time.sleep(3)
        self.drive.click('xpath', '//*[@id="scroll1"]/div[1]/div[1]/a')
        time.sleep(5)
        

if __name__ == '__main__':
#     pass
    baas = raybaas_function(down_dir='F:\\download', driver="chrome")
#     baas.drive.setWindowSize('max')
#     
#     baas.login('Admin', baas.s_user, baas.s_pass)
#     time.sleep(3)
    baas.login('User', baas.c_user, baas.c_pass)
#     if(baas.user_exist('mrray1')==None):
#         baas.add_user('mrray1', '123qaz', 'aaa@bbbxa.ccc', 'user')
    time.sleep(3)
#     
#     userExist = baas.user_exist('mrray1')
#     print(userExist)
# #     baas.logout()
#     if(baas.server_exist('192.168.1.166')==None):
#         baas.add_server('247', '192.168.1.166', '22', 'root', 'mrray@2020')
#     
#     if(baas.server_exist('192.168.1.247')==None):
#         baas.add_server('247', '192.168.1.247', '22', 'root', 'mrray@2020')
# #         
# #     time.sleep(3)
#     if(baas.server_exist('192.168.1.247')!=None):
#         baas.server_del('192.168.1.247')
#     server = baas.server_exist('192.168.1.247')
#     print(server)
#     baas.order_apply('首页', '哈利波特', 'D:\CLionhh_jb51.rar')
#     time.sleep(3)
# 
#     baas.chain_applay('perilong', 3, 1, 'kafka')
#     baas.chain_applay('perilong', 3, 1, 'kafka')
#     baas.chain_applay('perilong', 3, 1, 'raft')
#     baas.chain_applay('mrray', 3, 1, 'pbft')
#     baas.chain_applay('perilong', 3, 1, 'pbft')
#     for i in range(5):
#         baas.chain_del('perilong')

    p_n = baas.chain_peer_num('mrray')
    print(p_n)
      
    baas.drive.quit()
    
#     baas = raybaas_function(driver="firefox", down_dir='F:\download')
# #     baas = raybaas_function(driver="chrome")
#     baas.login('Admin', baas.s_user, baas.s_pass)
# #     time.sleep(3)
# #     
# #     baas.order_download_attach()
#     baas.chain_audit('mrray')
#     time.sleep(5)
#     baas.chain_deploy('mrray')
# #     
#     baas.drive.quit()
    