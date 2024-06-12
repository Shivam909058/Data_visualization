import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title='Data Visualizer', layout='wide', page_icon='📊')


st.title('Data Visualization Web App')


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:

    encodings = ['utf-8', 'latin1', 'utf-16']
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)
            break
        except UnicodeDecodeError:
            if enc == encodings[-1]:  # If it's the last encoding in the list
                st.error("Failed to read file with different encodings.")
            continue

    columns = df.columns.tolist()

  
    dashboard_plots = st.container()

    def generate_plot(df, x_axis, y_axis, plot_type):
        fig, ax = plt.subplots(figsize=(6, 4))
        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            y_axis = 'Density'
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            y_axis = 'Count'
        elif plot_type == 'Box Plot':
            sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Violin Plot':
            sns.violinplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Heatmap':
            sns.heatmap(df.corr(), annot=True, ax=ax)
        elif plot_type == 'KDE Plot':
            sns.kdeplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Joint Plot':
            sns.jointplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Swarm Plot':
            sns.swarmplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Point Plot':
            sns.pointplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Strip Plot':
            sns.stripplot(x=df[x_axis], y=df[y_axis], ax=ax)

        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)
        st.pyplot(fig)

    with st.sidebar:
        st.header('Plot Settings')
        num_plots = st.number_input('Number of plots', min_value=1, max_value=10, value=1, step=1)
        plot_settings = []
        for i in range(num_plots):
            plot_type = st.selectbox(f'Select plot type for Plot {i+1}', 
                                     ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 
                                      'Box Plot', 'Violin Plot', 'Heatmap', 'KDE Plot', 'Joint Plot', 
                                      'Swarm Plot', 'Point Plot', 'Strip Plot'], key=f'plot_type_{i}')
            x_axis = st.selectbox(f'Select the X-axis for Plot {i+1}', options=columns + ["None"], key=f'x_axis_{i}')
            y_axis = st.selectbox(f'Select the Y-axis for Plot {i+1}', options=columns + ["None"], key=f'y_axis_{i}')
            plot_settings.append((plot_type, x_axis, y_axis))

    st.write("### Data Preview")
    st.dataframe(df.head())

    with dashboard_plots:
        st.write("## Dashboard")
        for i, (plot_type, x_axis, y_axis) in enumerate(plot_settings):
            col1, col2 = st.columns(2)
            if i % 2 == 0:
                with col1:
                    generate_plot(df, x_axis, y_axis, plot_type)
            else:
                with col2:
                    generate_plot(df, x_axis, y_axis, plot_type)
