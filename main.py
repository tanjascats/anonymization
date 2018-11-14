import src.SaNGreeA as sangria


def main():
    # here goes definition of all config files and loop that runs the algorithm for each of them
    for k in range(40, 50):
        config_file = "config/config_" + str(k)
        sangria.run(config_file)
    # sangria.run("../config/config_test")
    #sangria.run("./config/config_28")


if __name__ == '__main__':
    main()
