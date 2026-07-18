export type CurrentStateItem = {
    metric_key: string;
    metric_type: string;
    value: number;
    timestamp: string;
};

export type Device = {
    id: number;
    dev_eui: string;
    name: string;
    profile_name: string;
    current_state: CurrentStateItem[];
}

export type Reading = {
    id: number;
    metric_key: string;
    metric_type: string;
    value: number;
    timestamp: string;
}