# coding=utf-8
from __future__ import print_function
import sys
import os
import torch
import traceback
from torch.autograd import Variable
import torch.nn as nn
import torch.backends.cudnn as cudnn
import importlib, argparse
from datetime import datetime
import multiprocessing
from ast import literal_eval
from comm.registry import Registry

from compute import Config_ini


class TrainModel(object):
    def __init__(self, file_id, logger):

        # module_name = 'scripts.%s'%(file_name)
        module_name = file_id
        if module_name in sys.modules.keys():
            self.log_record('Module:%s has been loaded, delete it' % (module_name))
            del sys.modules[module_name]
            _module = importlib.import_module('.', module_name)
        else:
            _module = importlib.import_module('.', module_name)

        net = _module.EvoCNNModel()
        cudnn.benchmark = True
        net = net.cuda()
        criterion = nn.CrossEntropyLoss()
        best_acc = 0.0
        self.net = net

        TrainConfig.ConfigTrainModel(self)
        # initialize optimizer
        opt_cls = Registry.OptimizerRegistry.query(Config_ini.optimizer)
        opt_params = {'name': Config_ini.optimizer}
        lr_cls = Registry.LRRegistry.query(Config_ini.lr_strategy)
        lr_params = {'lr': Config_ini.lr, 'lr_strategy': Config_ini.lr_strategy}
        lr_params['lr'] = float(lr_params['lr'])
        opt_params['lr'] = float(lr_params['lr'])
        self.opt_params = opt_params
        self.opt_cls = opt_cls
        self.opt_params['total_epoch'] = self.nepochs
        self.lr_params = lr_params
        self.lr_cls = lr_cls
        # after the initialization

        self.criterion = criterion
        self.best_acc = best_acc

        self.file_id = file_id
        self.logger = logger

    def log_record(self, _str):
        dt = datetime.now()
        dt.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info('[%s]-%s' % (dt, _str))

    def get_optimizer(self, epoch):
        # get optimizer
        self.opt_params['current_epoch'] = epoch
        opt_cls_ins = self.opt_cls(**self.opt_params)
        optimizer = opt_cls_ins.get_optimizer(filter(lambda p: p.requires_grad, self.net.parameters()))
        return optimizer

    def get_learning_rate(self, epoch):
        self.lr_params['optimizer'] = self.get_optimizer(epoch)
        self.lr_params['current_epoch'] = epoch
        lr_cls_ins = self.lr_cls(**self.lr_params)
        learning_rate = lr_cls_ins.get_learning_rate()
        return learning_rate

    def train(self, epoch):
        self.net.train()
        optimizer = self.get_optimizer(epoch)
        running_loss = 0.0
        total = 0
        correct = 0
        for _, data in enumerate(self.trainloader, 0):
            inputs, labels = data
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            optimizer.zero_grad()
            outputs = self.net(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * labels.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels.data).sum().item()
        self.log_record('Train-Epoch:%3d,  Loss: %.3f, Acc:%.3f' % (epoch + 1, running_loss / total, (correct / total)))

    def main(self, epoch):
        self.net.eval()
        test_loss = 0.0
        total = 0
        correct = 0
        for _, data in enumerate(self.validate_loader, 0):
            inputs, labels = data
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            outputs = self.net(inputs)
            loss = self.criterion(outputs, labels)
            test_loss += loss.item() * labels.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels.data).sum().item()
        if correct / total > self.best_acc:
            self.best_acc = correct / total
        self.log_record('Valid-Epoch:%3d, Loss:%.3f, Acc:%.3f' % (epoch+1, test_loss / total, correct / total))

    def process(self):
        total_epoch = self.nepochs
        scheduler = self.get_learning_rate(total_epoch)
        for p in range(total_epoch):
            scheduler.step()
            self.train(p)
            self.main(p)
        return self.best_acc


class RunModel(object):

    def log_record(self, _str):
        dt = datetime.now()
        dt.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info('[%s]-%s' % (dt, _str))

    def do_work(self, gpu_id, file_id, uuid):
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id
        logger = RedisLog(os.path.basename(file_id) + '.txt')
        best_acc = 0.0
        try:
            m = TrainModel(file_id, logger)
            m.log_record(
                'Used GPU#%s, worker name:%s[%d]' % (gpu_id, multiprocessing.current_process().name, os.getpid()))
            best_acc = m.process()
        except BaseException as e:
            msg = traceback.format_exc()
            print('Exception occurs, file:%s, pid:%d...%s' % (file_id, os.getpid(), str(e)))
            print('%s' % (msg))
            dt = datetime.now()
            dt.strftime('%Y-%m-%d %H:%M:%S')
            _str = 'Exception occurs:%s' % (msg)
            logger.info('[%s]-%s' % (dt, _str))
        finally:
            dt = datetime.now()
            dt.strftime('%Y-%m-%d %H:%M:%S')
            _str = 'Finished-Acc:%.3f' % best_acc
            logger.info('[%s]-%s' % (dt, _str))

            logger.write_file('RESULTS', 'results.txt', '%s=%.5f\n' % (file_id, best_acc))
            _str = '%s;%.5f\n' % (uuid, best_acc)
            logger.write_file('CACHE', 'cache.txt', _str)


if __name__ == "__main__":
    ls_dataset = ['MNIST', 'CIFAR10', 'CIFAR100']
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-gpu_id", "--gpu_id", help="GPU ID", type=str)
    _parser.add_argument("-file_id", "--file_id", help="file id", type=str)
    _parser.add_argument("-uuid", "--uuid", help="uuid of the individual", type=str)

    _parser.add_argument("-super_node_ip", "--super_node_ip", help="ip of the super node", type=str)
    _parser.add_argument("-super_node_port", "--super_node_port", help="port of the redis", type=str)
    _parser.add_argument("-super_node_pid", "--super_node_pid", help="pid on the super node", type=str)
    _parser.add_argument("-worker_node_ip", "--worker_node_ip", help="ip of this worker node", type=str)

    _parser.add_argument("-train_dataset", "--train_dataset", help="dataset of train", type=str)
    _parser.add_argument("-train_data_dir", "--train_data_dir", help="dir of trained dataset", type=str)
    _parser.add_argument("-data_input_size", "--data_input_size", help="input size of train data", type=str)

    _parser.add_argument("-train_optimizer", "--train_optimizer", help="optimizer of train", type=str)
    _parser.add_argument("-train_lr", "--train_lr", help="learning rate of train", type=str)
    _parser.add_argument("-train_batch_size", "--train_batch_size", help="batch_size of train", type=str)
    _parser.add_argument("-train_total_epoch", "--train_total_epoch", help="total_epoch of train", type=str)
    _parser.add_argument("-train_lr_strategy", "--train_lr_strategy", help="lr_strategy of train", type=str)

    _args = _parser.parse_args()
    Config_ini.log_server = _args.super_node_ip
    Config_ini.log_server_port = int(_args.super_node_port)
    Config_ini.dataset = _args.train_dataset
    if Config_ini.dataset not in ls_dataset:
        Config_ini.data_dir = _args.train_data_dir
        Config_ini.img_input_size = [int(_args.data_input_size.split(',')[i])
                                     for i in range(len(_args.data_input_size.split(',')))]
    Config_ini.optimizer = _args.train_optimizer
    Config_ini.lr = float(_args.train_lr)
    Config_ini.batch_size = int(_args.train_batch_size)
    Config_ini.total_epoch = int(_args.train_total_epoch)
    Config_ini.lr_strategy = _args.train_lr_strategy
    from compute import Config_ini
    from compute.redis import RedisLog
    from compute.pid_manager import PIDManager, PIDRedis
    from algs.performance_pred.utils import TrainConfig

    PIDManager.WorkerEnd.add_worker_pid(_args.super_node_ip, _args.super_node_pid, _args.worker_node_ip)

    RunModel().do_work(_args.gpu_id, _args.file_id, _args.uuid)

    PIDManager.WorkerEnd.remove_worker_pid(_args.super_node_ip, _args.super_node_pid, _args.worker_node_ip)
