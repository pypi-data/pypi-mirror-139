# ONNXExplorer


**onnxexp** is an easy way to explore your onnx model. It helps you debug and even convert/inference your onnx simply with a single command line.

![](https://s4.ax1x.com/2022/02/10/HNe5MF.png)

Now, you have another option to *view, debug, summary* your model without netron. You can also using this tool converts your model to trt engine.

You can install `onnxexplorer` simply by:

```
pip install onnxexplorer
```

then you can using `onnxexp -h` to see what it capable of:

```
usage: onnxexp [-h] [--version] {glance,totrt,check} ...

positional arguments:
  {glance,totrt,check}
    glance              Take a glance at your onnx model.
    totrt               Convert your model to trt using onnx-tensorrt python
                        API.
    check               Check your onnx model is valid or not.

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show version info.
```


The final function onnxexp will provide are:

- [x] Glance at your onnx model info, print out input and output shapes information, and Node sets;
- [x] Search node detail by provide node id, or node type, etc, search all `Conv` in your model;
- [ ] Int8 convert of your onnx model;
- [x] Convert your model to tensorrt via onnx-tensorrt python API;
- [ ] Calculate your model params and test speed via ONNXRuntime;



## Update

- **2021.12.22**: Add TensorRT convert function, now you can using `onnxexp` convert your onnx model to trt engine, even with dynamic input models:
  ```
  onnxexp totrt -m shufflenetv2_body.onnx --min_shapes img:1x3x384x288 --opt_shapes img:2x3x384x288 --max_shapes img:4x3x384x288
  ```
- **2021.12.04**: Update args, re-organised readme and usage;
- **2021.01.06**: Update search functions;
- **2019.09.30**: First released this package;



## Install

to install *onnxexplorer*, you can do:

```
sudo pip3 install onnxexplorer
```

Or if pip not available:

```
sudo python3 setup.py install
```



## Copyright

All right reserved by Lucas Jin. Codes released under Apache License.