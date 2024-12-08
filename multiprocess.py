from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):
        self.manager = Manager()
        self.data = self.manager.dict()  # Используем менеджер для создания разделяемого словаря

    def process_request(self, request):
        product, action, quantity = request
        if action == "receipt":
            # Обработка поступления товара
            if product in self.data:
                self.data[product] += quantity
            else:
                self.data[product] = quantity
        elif action == "shipment":
            # Обработка отгрузки товара
            if product in self.data and self.data[product] >= quantity:
                self.data[product] -= quantity

    def run(self, requests):
        processes = []
        for request in requests:
            p = Process(target=self.process_request, args=(request,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()



if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    manager.run(requests)


    print(dict(manager.data))