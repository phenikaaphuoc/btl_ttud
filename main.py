import numpy as np
import copy
import matplotlib.pyplot as plt
import random
class Solver:
    def __init__(self,data_path):
        with open(data_path,"r") as f:
            #đọc số chi tiết cần lắp
            self.n = int(f.readline().strip())
            #đọc dữ liệu và chuyển thành numpy
            self.coss_matrix = np.array([[int(i) for i in value.strip().split(" ")] for value in f.readlines()])
            #khởi tạo machine rỗng 
            self.name_machines = ['A','B','C']
            self.num_machines = len(self.name_machines)
            self.machines = {}
            for name_machine in self.name_machines:
                self.machines[name_machine] = []
           
        self.init_solution("random_init")
        print("cost init: ",self.calculate_total_cost())
        self.optimize()
        self.plot_solution()
    def optimize(self,max_so_lan_khong_giam = 10):
        #dùng để kiểm tra điều kiện dừng
        self.so_lan_khong_giam = 0
        while True:
            #tính chi phí lúc đầu 
            span  = self.calculate_total_cost()
            #chọn ngẫu nhiên loại thay đổi 
            random_choice = random.randint(0,1)
            if random_choice:
                
                #thực hiện thay đổi
                self.local_search_first_move()
                #tính chi phí mới
              
                    
            else:
                self.local_search_swap()
            span_new = self.calculate_total_cost()    
               
            #nếu không tốt hơn tăng điều kiện dừng
            if span_new >= span:
                self.so_lan_khong_giam+=1
                print("So lan khong giam : ",self.so_lan_khong_giam)
            else:
                print("get better cost: ",span_new)
            #kiểm tra điều kiện dừng
            if self.so_lan_khong_giam > max_so_lan_khong_giam:
                
                break
                
                


    def init_solution(self,type = "min_time_init"):
        #khởi tạo solution theo nhiều cách
        getattr(self,type)()
       
 
    def get_min_machine(self,job_index : int) -> int:
        machine_index = np.argmin(self.coss_matrix[:,job_index])
        return machine_index
    def min_time_init(self):
         # duyệt tất cả các chi tiết
        for i in range(self.n):
            #chonj ra máy có chi phí ít nhất
            min_machine = self.get_min_machine(i)
            name_machine = self.name_machines[min_machine]
            # thêm vào machine
            self.machines[name_machine].append(i)
    def random_init(self):
        # duyệt tất cả các chi tiết
        for i in range(self.n):
            #chọn tuần tự các máy tương ứng (chia dư)
            name_machine = self.name_machines[i%self.num_machines]
            # thêm vào machine
            self.machines[name_machine].append(i)

    def local_search_best_move(self):
        # Perform a local search by moving a job from one machine to another
        best_solution = copy.deepcopy(self.machines)  # Make a copy of the current solution
        best_cost = self.calculate_total_cost()

        # Iterate through all machines and jobs
        for from_machine in self.name_machines:
            for to_machine in self.name_machines:
                if from_machine != to_machine:
                    for job_index in range(len(self.machines[from_machine])):
                        # Try moving the job from 'from_machine' to 'to_machine'
                        temp_solution = copy.deepcopy(self.machines)
                        job = temp_solution[from_machine].pop(job_index)
                        temp_solution[to_machine].append(job)

                        # Calculate the cost of the new solution
                        temp_cost = self.calculate_total_cost(temp_solution)

                        # Update the best solution if the new solution is better
                        if temp_cost < best_cost:
                            best_solution = copy.deepcopy(temp_solution)
                            best_cost = temp_cost

        # Update the current solution with the best solution found
        self.machines = best_solution
    def local_search_first_move(self):
        best_cost = self.calculate_total_cost()

        # Iterate through all machines and jobs
        for from_machine in self.name_machines:
            for to_machine in self.name_machines:
                # Nếu cùng 1 máy skip
                if from_machine != to_machine:
                    for job_index in range(len(self.machines[from_machine])):
                        # Try moving the job from 'from_machine' to 'to_machine'
                        temp_solution = copy.deepcopy(self.machines)
                        job = temp_solution[from_machine].pop(job_index)
                        temp_solution[to_machine].append(job)

                        # Calculate the cost of the new solution
                        temp_cost = self.calculate_total_cost(temp_solution)

                        # Update the best solution if the new solution is better
                        if temp_cost < best_cost:
                            self.machines = copy.deepcopy(temp_solution)
                            return
    def local_search_swap(self):
        # Perform a local search by swapping one job from one machine with another job
        best_solution = copy.deepcopy(self.machines)  # Make a copy of the current solution
        best_cost = self.calculate_total_cost()

        # Iterate through all machines and jobs
        for machine1 in self.name_machines:
            for machine2 in self.name_machines:
                if machine1 != machine2:
                    for job_index1 in range(len(self.machines[machine1])):
                        for job_index2 in range(len(self.machines[machine2])):
                            # Try swapping job_index1 from machine1 with job_index2 from machine2
                            temp_solution = copy.deepcopy(self.machines)
                            job1 = temp_solution[machine1].pop(job_index1)
                            job2 = temp_solution[machine2].pop(job_index2)
                            temp_solution[machine1].append(job2)
                            temp_solution[machine2].append(job1)

                            # Calculate the cost of the new solution
                            temp_cost = self.calculate_total_cost(temp_solution)

                            # Update the best solution if the new solution is better
                            if temp_cost < best_cost:
                                best_solution = copy.deepcopy(temp_solution)
                                best_cost = temp_cost
                                # Accept the swap immediately if it results in a better solution
                                self.machines = best_solution
                                return
    def local_search_swap_n_times(self,n = 10):
        for _ in range(n):
            self.local_search_swap()
            
    def local_search_first_move_n_times(self, n=10):
        for _ in range(n):
            self.local_search_first_move()

    def local_search_best_move_n_times(self,n = 10):
        for _ in range(n):
            self.local_search_best_move()
        
    def calculate_total_cost(self, solution=None)-> float:
        # Calculate the total cost of the current solution or a given solution
        if solution is None:
            solution = self.machines

        total_cost = 0
        for machine_index,jobs in enumerate(solution.values()):
            for job_index in jobs:
                total_cost += self.coss_matrix[machine_index, job_index]

        return float(total_cost)
    def plot_solution(self, solution=None,loai_loi_giai = None):
    # show solution
        if solution is None:
            solution = self.machines
        fig, ax = plt.subplots()
        # Width of each bar
        bar_width = 0.2  # Adjust this value based on your preference
        # Initialize a dictionary to store cumulative processing times for each machine
        cumulative_times = {machine_name: [0] * len(self.name_machines) for machine_name in self.name_machines}
        # Iterate over machines and jobs
        for machine_index, machine_name in enumerate(self.name_machines):
            jobs = solution[machine_name]
            for job_index, job in enumerate(jobs):
                # Get the processing time for the current job on the current machine
                processing_time = self.coss_matrix[machine_index, job]

                # Calculate the x-coordinate for the bar
                x_coord = machine_index 

                # Plot a bar for each job with a different color and cumulative height based on processing time
                ax.bar(x_coord, processing_time, width=bar_width, color=plt.cm.viridis(job_index / self.n), bottom=cumulative_times[machine_name][machine_index], align='edge')

                
                # Accumulate processing time for the current job on the current machine
     
                ax.text(x_coord + bar_width / 2, cumulative_times[machine_name][machine_index] +processing_time//2, str(job), ha = "center", color='white', fontweight='bold')
                cumulative_times[machine_name][machine_index] += processing_time
        # Set labels and show the plot
        ax.set_ylabel('Time')
        ax.set_xlabel('Machines')
        if loai_loi_giai:
            title = f"{loai_loi_giai} co tong thoi gian {self.calculate_total_cost()}" 
        else:
            title = f"Span {self.calculate_total_cost()}"
        ax.set_title(title)
        ax.set_xticks(np.arange(len(self.name_machines)) + 0.5 * (len(self.name_machines) - 1) * bar_width)
        ax.set_xticklabels(self.name_machines)
        plt.show()




    def save_image_solution(self,solution = None):
         if solution is None:
            solution = self.machines
        
data_path = "data.txt"
solver = Solver(data_path=data_path)

