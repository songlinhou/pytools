def in_which_env():
    try:
        cfg = get_ipython().config
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return "jupyter"
        if cfg['IPKernelApp']['kernel_class'] == 'google.colab._kernel.Kernel':
            return "colab"
        else:
            return "ipython"
    except NameError:
        return "python"

def try_import(name):
    import subprocess
    subprocess.call("pip install {}".format(name),shell=True)