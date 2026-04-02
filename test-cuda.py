import torch

if torch.cuda.is_available():
    print("GPU detected:", torch.cuda.get_device_name(0))
    # Lista tipurilor de date suportate
    print("CUDA half support:", torch.cuda.get_device_properties(0).major >= 5)
    try:
        a = torch.randn(2, 2, device="cuda", dtype=torch.float16)
        print("FP16 works!")
    except Exception as e:
        print("FP16 not supported:", e)
else:
    print("No GPU detected, will use CPU")