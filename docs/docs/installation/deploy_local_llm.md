---
id: local-llm
title: Local LLM Deployment
sidebar_label: Local LLM Deployment
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

To create assistants that run entirely on your machine, you must run a model locally. We recommend the [OpenHermes-NeuralChat merged model](https://huggingface.co/Weyaxi/OpenHermes-2.5-neural-chat-v3-3-Slerp) that is 7 billion parameters and ~6GB. We have tested Rubra with this model, but you can use any model you want at your own risk. Let us know if you'd like support for other models by [opening up a Github issue](https://github.com/rubra-ai/rubra/issues/new)!

We leverage [llamafile](https://github.com/Mozilla-Ocho/llamafile) to distribute and run local LLMs.

## Prerequisites

Make sure you meeting the [prerequisites](./prerequisites) before you start.

## Setup
1. Manually download the Llamafile for your OS [from Hugging Face](https://huggingface.co/rubra-ai/rubra-llamafile/tree/main) or run this command:

    <Tabs groupId="operating-systems">
        <TabItem value="mac" label="macOS + Linux">
            ```shell
            curl -L -o rubra.llamafile https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/rubra.llamafile
            ```
        </TabItem>
        <TabItem value="win" label="Windows">
            Downloads 2 files: `llamafile.exe` and `openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf`
            Make sure you are using **[the correct curl command](https://medium.com/@boutnaru/the-windows-process-journey-curl-exe-curl-executable-87cfe60184b9)**
            ```shell
            curl -L -o llamafile.exe https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/llamafile.exe
            curl -L -o openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf
            ```
        </TabItem>
    </Tabs>


2. Give the file executable permissions:

    <Tabs groupId="operating-systems">
        <TabItem value="mac" label="macOS + Linux">
            ```shell
            chmod +x rubra.llamafile
            ```
        </TabItem>
        <TabItem value="win" label="Windows">
            `llamafile.exe` should be executable by default. However, if you find that the llamafile is not executable or you want to ensure that it has the correct permissions, you can adjust the file properties through the file explorer or use the `icacls` command in the command prompt to modify the file's access control lists.

            To set the execute permission on `llamafile.exe` using the GUI, you would:

                1. Right-click on the file and select "Properties."
                2. Go to the "Security" tab.
                3. Click on "Edit..." to change permissions.
                4. Select the user or group you want to grant execute permissions to.
                5. Check the "Allow" box for "Read & execute" under the "Permissions for Users" section.
                6. Click "Apply" and then "OK."
            ___
            To do something similar from the command line, you can use the `icacls` command:

            ```cmd
            icacls "llamafile.exe" /grant Everyone:RX
            ```
        </TabItem>
    </Tabs>

3. Run the model:
    
    <Tabs groupId="operating-systems">
        <TabItem value="mac" label="macOS + Linux">
            ```shell
            ./rubra.llamafile --ctx-size 16000
            ```
        </TabItem>
        <TabItem value="win" label="Windows">
            ```shell
            ./llamafile.exe -m openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf --ctx-size 16000 --host 0.0.0.0 --port 1234 --nobrowser -ngl 35
            ```
            * You must run the model on **port 1234**
        </TabItem>
    </Tabs>

    :::note
    * *(Optional)* Increase/decrease the context window size with the `--ctx-size` flag. The default is 16000. A larger context window size will increase the memory usage of the model but will result in high quality responses. Those without a GPU and/or limited RAM (i.e. 8 GB) should keep this value low.
    * GPU Support:
      * `-ngl` is the number of layers offloaded to the GPU. The default is 35. You can adjust this value to offload more/ess layers to the GPU. Add this to your command: `./rubra.llamafile --ctx-size 16000 -ngl 35`
      * Apple Silicon on MacOS
        * You need to have [Xcode Command Line Tools](https://mac.install.guide/commandlinetools/index.html) installed for llamafile to be able to bootstrap itself
        * If you use zsh and have trouble running llamafile, try running `sh -c ./rubra.llamafile --ctx-size 16000`. This is due to a bug that was fixed in zsh 5.9+
      * NVIDIA GPUs
        * Install [CUDA](https://developer.nvidia.com/cuda-downloads) and [cuDNN](https://developer.nvidia.com/cudnn) on your machine
      * AMD GPUs
        * Install the [ROCm SDK](https://rocm.docs.amd.com/en/latest/)
    :::

___

## Testing

Congrats! You have a model running on your machine. To test it out, you can run the following command:

```shell
curl http://localhost:1234/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer no-key" \
-d '{
  "messages": [
      {
          "role": "system",
          "content": "You are a friendly assistant"
      },
      {
          "role": "user",
          "content": "Hello world!"
      }
    ]
}'
```
