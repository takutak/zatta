import numpy as np
import torch
import torch.nn as nn

class NN(nn.Module):
    
    def __init__(self, n_input, n_output, neuron_per_layer=50):
        
        super(NN, self).__init__()
        
        self.activation = nn.Tanh()
        
        self.n_input = n_input
        self.n_output = n_output
        
        self.affine1 = nn.Linear(self.n_input, neuron_per_layer)
        self.affine2 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine3 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine4 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine5 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine6 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine7 = nn.Linear(neuron_per_layer, neuron_per_layer)
        self.affine8 = nn.Linear(neuron_per_layer, self.n_output)
        
    
    def forward(self, t):
        
        t = self.activation(self.affine1(t))
        t = self.activation(self.affine2(t))
        t = self.activation(self.affine3(t))
        t = self.activation(self.affine4(t))
        t = self.activation(self.affine5(t))
        t = self.activation(self.affine6(t))
        t = self.activation(self.affine7(t))
        t = self.affine8(t)
        
        return t
class PINNs():
    
    def __init__(self, t, t_region, x, x_region, u, nu):
        
        self.nu = nu

        self.t = torch.tensor(t, requires_grad=True).float()
        self.t_region = torch.tensor(t_region, requires_grad=True).float() 
        self.x = torch.tensor(x, requires_grad=True).float()
        self.x_region = torch.tensor(x_region, requires_grad=True).float()
        self.u = torch.tensor(u, requires_grad=True).float()
        

        self.dnn = NN(2, 1)
        
        self.optimizer = torch.optim.Adam(self.dnn.parameters(), lr=1e-3)

    def net_u(self, x, t):
        u = self.dnn(torch.cat([x, t], dim=1))
        return u

    def net_f(self, x, t):
        
        u = self.net_u(x, t)
        
        #時間1階微分
        u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u),retain_graph=True, create_graph=True)[0]
        #空間１階微分
        u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u),retain_graph=True, create_graph=True)[0]
        #空間２回微分
        u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x),retain_graph=True, create_graph=True)[0]
        
        f = u_t + u * u_x - self.nu * u_xx 
        
        return f
    
    #損失の評価
    def loss_func(self):
            
        u_pred = self.net_u(self.x, self.t)
        f_pred = self.net_f(self.x_region, self.t_region)
        loss_u = torch.mean((self.u - u_pred)**2)
        loss_f = torch.mean(f_pred**2)
        
        loss = loss_u + loss_f*5e-4
        
        return loss, loss_u, loss_f
    
    # 学習
    def train(self):
        
        epochs = 20000
        for epoch in range(epochs):
            
            self.dnn.train()
            
            self.loss, self.loss_u, self.loss_f = self.loss_func()
            self.loss.backward()
            self.optimizer.step()
            
            self.optimizer.zero_grad()
            
            if epoch % 100 ==0:
                print( 'Iter %d, Loss: %.5e, Loss_u: %.5e, Loss_f: %.5e' % (epoch, self.loss.item(), self.loss_u.item(), self.loss_f.item()))
            
    # 予測
    def predict(self, x, t):

        x = torch.tensor(x, requires_grad=True).float()
        t = torch.tensor(t, requires_grad=True).float()
        
        #評価モードに変更
        self.dnn.eval()

        u = self.net_u(x, t).detach().numpy()
        f = self.net_f(x, t).detach().numpy()
        
        
        return u, f