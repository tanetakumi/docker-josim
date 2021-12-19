# docker-josim

This is a container for easy installation of josim and analysis of simulation results in python.

JoSIM is able to recognize pi junctions.

[JoSIM](https://github.com/JoeyDelp/JoSIM)

## Installation

1.  install Docker.  [Docker](https://www.docker.com/)

2.  Clone this repository or download it as a zip file
    ```
    git clone https://github.com/tanetakumi/docker-josim
    ```

3.  Build a container from the Dockerfile. (.devcontainer/Dockerfile)
    
    For easy installation, you can install "Remote - Containers" from the VScode extension, open the folder where you downloaded this repository, and open it from "Reopen in Container".

    [Remote - Containers](https://code.visualstudio.com/docs/remote/containers)

## Command

- if If you have the X11 client installed on your computer, you can easily view the simulation results in a graph by running this command.
    ```
    sim-plot <filepath>
    ```

- Circuit Optimization Commands

    under development
    ```
    optimize <filepath> <outputfilepath>
    ```
