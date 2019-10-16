package main

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/urfave/cli"
)

func main() {
	app := cli.NewApp()
	app.Name = "git-pusher-go"
	app.Usage = "This app is for wrapper for git push"
	app.Version = "0.0.1"

	app.Action = func(context *cli.Context) error {
		out, err := exec.Command("git", "rev-parse", "--abbrev-ref", "HEAD").Output()
		if err != nil {
			fmt.Println(err)
		}

		fmt.Println(string(out))

		return nil
	}

	app.Run(os.Args)
}
