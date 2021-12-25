import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
acesslog = "./access.log"
errorlog = "./error.log"

max_requests = 100
