export BASHGPT_NAME="bashgpt"


function _exec(){
    command=$1
    echo "$command"
    $command
}


function build_tool(){
    version="$1"
    build_path="builds/$BASHGPT_NAME-$version"

    echo "Starting build..."
    echo "Version: $version"
    echo "Path: $build_path"

    if [ ! -d "builds" ]; then
        mkdir builds
    fi

    if [ -d $build_path ]; then
        echo "WARNING: Build directory already exists: $build_path"
        rm -rf $build_path

    fi
    mkdir "$build_path"
    mkdir "$build_path/DEBIAN"
    mkdir -p "$build_path/usr/share/$BASHGPT_NAME"
    mkdir -p "$build_path/usr/bin"

    cp -r debian/* "$build_path/DEBIAN"
    cp -r bashgpt/src/* "$build_path/usr/share/bashgpt"
    cp bashgpt/bin/gpt "$build_path/usr/bin/"
    cp -r bashgpt/config "$build_path/usr/share/bashgpt"

    chmod +x "$build_path/usr/bin/gpt"

    dpkg-deb --build $build_path

    sudo apt remove -y bashgpt
    sudo dpkg -i builds/$BASHGPT_NAME-$version.deb

    echo "Build completed successfully!"
}
