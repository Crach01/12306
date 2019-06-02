# encoding = utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Qiangpiao(object):

    def __init__(self):
        self.student = 1
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.init_my_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.driver = webdriver.Chrome(
            executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def wait_input(self):

        self.from_station = input("起始站：")
        self.to_station = input("目的地：")
        # 时间格式：yyyy-mm-dd
        self.depart_time = input("出发时间：格式(yyyy-mm-dd)")
        self.passengers = input("输入乘车人姓名：(多个人用英文逗号隔开)").split(",")
        self.trains = input("车次：(多个车次用英文逗号隔开)").split(',')
        self.student = int(input("是否买学生票(学生票输入1，普通票输入0)"))

    def _login(self):
        self.driver.get(self.login_url)
        # 显示等待
        WebDriverWait(self.driver, 1000).until(
            EC.url_to_be(self.init_my_url)
        )
        print("登陆成功")

    def _order_ticket(self):
        # 1、跳转到查询余票的界面
        self.driver.get(self.search_url)

        # 2、等待出发地正确输入
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "fromStationText"), self.from_station)
        )
        # 3、等待目的地正确输入
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.to_station)
        )
        # 4、等待输入等待日期
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time)
        )

        # WebDriverWait(self.driver, 1000).until(
        #     EC.element_to_be_clickable((By.ID, "sf2"))
        # )
        # btn = self.driver.find_element_by_id("sf2")
        # btn.click()

        # 5、等待查询按钮是否可用
        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "query_ticket"))
        )
        # 6、如果能够被点击，那么就点击这个查询按钮，执行点击事件
        search_btn = self.driver.find_element_by_id("query_ticket")
        search_btn.click()

        # 7、在点击查询按钮之后，等待车次信息是否都显示出来了
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, ".//tbody[@id='queryLeftTable']/tr"))
        )
        # 8、找到所有没有datatrain属性的tr标签，这些标签是存储了车次信息的
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")

        # 9、便利所有满足条件的tr标签
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            if train_number in self.trains:
                left_ticket_td = tr.find_element_by_xpath(".//td[4]").text
                if left_ticket_td == '有' or left_ticket_td.isdigit:
                    order_btn = tr.find_element_by_class_name("btn72")
                    order_btn.click()

                    # 等待是否来到确认乘客信息页面
                    WebDriverWait(self.driver, 1000).until(
                        EC.url_to_be(self.passenger_url)
                    )
                    # 等待所有乘客信息是否都被加载进来
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.XPATH, ".//ul[@id='normal_passenger_id']/li"))
                    )

                    # 查看所有的乘客信息
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()

                    # 选择学生证信息
                    if self.student == 1:
                        WebDriverWait(self.driver, 1000).until(
                            EC.presence_of_element_located((By.ID, "dialog_xsertcj_ok"))
                        )
                        student_btn = self.driver.find_element_by_id("dialog_xsertcj_ok")
                        student_btn.click()


                    # 获取提交订单按钮 李东雷(学生)
                    submit_btn = self.driver.find_element_by_id("submitOrder_id")
                    submit_btn.click()

                    # 判断提交对话框是否被加载进来
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dhtmlx_wins_body_outer"))
                    )
                    # 显示等待，判断确认订单按钮是否出现
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.ID, "qr_submit_id"))
                    )

                    
                    confirm_btn = self.driver.find_element_by_id("qr_submit_id")
                    confirm_btn.click()
                    # while confirm_btn:
                    #     confirm_btn.click()
                    #     confirm_btn = self.driver.find_element_by_id("qr_submit_id")

                    return

    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = Qiangpiao()
    spider.run()
