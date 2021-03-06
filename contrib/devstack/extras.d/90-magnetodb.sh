if is_service_enabled magnetodb; then
    if [[ "$1" == "source" ]]; then
        # Initial source
        source $TOP_DIR/lib/magnetodb
    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Magnetodb"
        install_magnetodb
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Magnetodb"
        configure_magnetodb
        create_magnetodb_credentials
        if is_service_enabled tempest; then
            configure_magnetodb_tempest_plugin
        fi
    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        echo_summary "Starting Magnetodb"
        start_magnetodb
    fi

    if [[ "$1" == "unstack" ]]; then
        echo "Stopping MagnetoDB"
        stop_magnetodb
        echo "Cleaning MagnetoDB data"
        clean_magnetodb
    fi

    if [[ "$1" == "clean" ]]; then
        echo "Cleaning Magnetodb"
        clean_magnetodb
    fi
fi
