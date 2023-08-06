
class SessionInfo:
    dataset = ''
    device = ''
    part = ''
    lr = 1
    loss = ''
    batchsize = 0
    optimizer = ''
    momentum = ''

    def __init_(self, dataset, device, part, lr, loss, batchsize, optimizer, momentum):
        self.dataset = dataset
        self.device = device
        self.part = part
        self.lr = lr
        self.loss = loss
        self.batchsize = batchsize
        self.Optimizer = optimizer
        self.Momentum = momentum