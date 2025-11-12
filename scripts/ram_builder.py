import pandas as pd

WRAM_WEIGHTS = {
    'C': 3,  # Control
    'P': 3,  # Precondition
    'T': 2,  # Time
    'I': 1,  # Input
    'R': 1   # Resource
}

P_EXEC_DICT = {
    'to monitor (by captain)': 0.95,
    'to instruct helmsman': 0.9,
    'maneuvering / to depart': 0.9,
    'maneuvering / to arrive': 0.9,
    'to control the rudder': 0.9,
    'to do bow and aft work': 0.85,
    'to prepare the engine': 0.8,
    'to control the engine': 0.8,
    'to communicate with engine dept.': 0.7,
    'to communicate with deck dept.': 0.7,
    'maneuvering': 0.3,
    'to communicate with other ship': 0.1,
    'to communicate with vts': 0.05,
    'to follow the rules': 1.0,
    'to watch the vicinity': 1.0,
    'to watch the electronic devices': 1.0,
    'to do direct lookout': 1.0,
    'to pay attention to the vhf radio': 1.0,
    'to monitor the weather condition': 1.0,
    'briefing': 0.95,
    'to perform checklist': 0.95,
    'to board the ship': 0.99,
    'to monitor (by oow)': 0.95,
    'to take over the bridge control': 0.8,
    'standby (captain)': 0.8
}

def main():
    df = pd.read_csv('data/couplings_data.csv')
    df['Upstream_Function'] = df['Upstream_Function'].str.lower().str.strip()
    df['Downstream_Function'] = df['Downstream_Function'].str.lower().str.strip()
    df['Aspect_Type'] = df['Aspect_Type'].str.upper().str.strip()
    df['Context'] = df['Context'].str.strip()

    for context, df_ctx in df.groupby('Context'):
        df_ctx = df_ctx.reset_index(drop=True)
        df_ctx['Coupling_ID'] = df_ctx.index + 1

        coupling_ids = df_ctx['Coupling_ID'].tolist()
        n = len(coupling_ids)

        RAM_Matrix = pd.DataFrame(0, index=coupling_ids, columns=coupling_ids)
        WRAM_Matrix = pd.DataFrame(0, index=coupling_ids, columns=coupling_ids)

        # RAM/WRAM行列の構築
        for i, row_i in df_ctx.iterrows():
            for j, row_j in df_ctx.iterrows():
                if row_i['Upstream_Function'] == row_j['Downstream_Function']:
                    RAM_Matrix.loc[row_i['Coupling_ID'], row_j['Coupling_ID']] = 1
                    # i行j列のAspect_Typeで重みを取得
                    weight = WRAM_WEIGHTS.get(row_j['Aspect_Type'], 1)
                    WRAM_Matrix.loc[row_i['Coupling_ID'], row_j['Coupling_ID']] = weight

        RAM_Matrix.index.name = 'Coupling_ID'
        RAM_Matrix.columns.name = 'Coupling_ID'
        WRAM_Matrix.index.name = 'Coupling_ID'
        WRAM_Matrix.columns.name = 'Coupling_ID'

        RAM_Matrix.to_csv(f'output_RAM_matrix_{context}.csv')
        WRAM_Matrix.to_csv(f'output_WRAM_matrix_{context}.csv')

if __name__ == '__main__':
    main()