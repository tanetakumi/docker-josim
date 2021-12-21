# docker-josim

This is a container that contains josim, python and other tools.

JoSIM is a SPICE syntax circuit simulator specifically created to handle superconducting elements such as the Josephson junction

Now, circuits containing pi-junctions(ferromagnetic junctions) can also be simulated.

[JoSIM](https://github.com/JoeyDelp/JoSIM)

## Installation

1.  install Docker.  　[Docker](https://www.docker.com/)

2.  Clone this repository or download it as a zip file
    ```
    git clone https://github.com/tanetakumi/docker-josim
    ```

3.  Build a container from the Dockerfile. (.devcontainer/Dockerfile)
    
    For easy installation, I recommend you to use VScode.
    
    First, please install Remote- Containers[Remote - Containers](https://code.visualstudio.com/docs/remote/containers) from VScode extensions.
    ![image](https://user-images.githubusercontent.com/75787495/146673520-c86cc686-21ef-4cdd-a06e-8edb493877ce.png)
    
    Open the folder where you have downloaded this repository and click on the green button on the bottom left.
    
    ![image](https://user-images.githubusercontent.com/75787495/146674126-021c88c3-8ce1-4b29-b6b6-87ce5271460e.png)

    Select "Reopen in container".
    
    ![image](https://user-images.githubusercontent.com/75787495/146674076-fbd9f7ea-b333-428b-ad3e-62f2d246bbd6.png)
    
    Just wait a few minutes.


## Functions

- josim
- x11 forwarding
- python
- simulation and plot
- optimize

## Command

- Simulation and plot command

    If you have the X11 client installed on your computer, you can easily view the simulation results in a graph by running this command.
    ```
    simplot <filepath>
    ```

- Circuit Optimization Commands

    under development
    ```
    optimize <filepath>
    ```
