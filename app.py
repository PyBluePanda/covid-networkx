import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.buy_me_a_coffee import button
import warnings 

from model import create_interactive_plot, create_results_plot

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide",
    page_title="Covid - x - NetworkX", page_icon=":microbe:", 
    initial_sidebar_state="collapsed",
)


with stylable_container(
    key="title_container",
    css_styles="""
        {
            padding: calc(1em - 1px);
            text-align: center;
        }
        """,
):
    st.markdown('''# :blue[Covid - x - NetworkX] :microbe:''')


with stylable_container(
    key="key_container",
    css_styles="""
        {
            border: 0.1px solid rgba(80, 80, 80, 0.5);
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            text-align: center;
            background-color: #001832;
        }
        """,
):
    st.markdown('''
    :blue[S] :orange[E] A :red[I] :green[R] - 
    :blue[Susceptible] /
    :orange[Exposed (latent) phase] /
    Asymptomatic spreaders / 
    :red[Infected (symptomatic) individuals] /
    :green[Recovered (immunity gained)]
    ''')

app_col1, app_col2 = st.columns([3,10], vertical_alignment="top")

with app_col1:

    # ==== data input form ====

    form = st.form(key="form_settings")
    
    network_type = form.selectbox(
        "Network Type",
        options=["small-world","scale-free","random", 
                 "complete", "cycle", "lollipop"],
        key="network_type",
        placeholder="small-world"
    )

    form_col1, form_col2 = form.columns([3,3])

    N = form_col1.number_input(
        "Number of people",
        10,
        150,
        step=10,
        key="N",
        value=40
    )

    timesteps = form_col2.number_input(
        "Simulation steps",
        20,
        80,
        step=5,
        key="timesteps",
        value=40
    )

    incubation_period = form_col1.slider(
        "Incubation period",
        1,
        10,
        step=1,
        key="incubation_period",
        value=3
    ) 

    recovery_time = form_col2.slider(
        "Recovery time",
        1,
        10,
        step=1,
        key="recovery_time",
        value=7
    ) 

    p_asymptomatic = form_col2.slider(
        "p_asymptomatic",
        0.0,
        1.0,
        step=.1,
        key="p_asymptomatic",
        value=0.3
    ) 

    p_transmission = form_col1.slider(
        "p_transmission",
        0.0,
        1.0,
        step=.1,
        key="p_transmission",
        value=0.3
    ) 

    # ==== end of data input ====

    params = {
        "N":N,
        "timesteps":timesteps,
        "p_asymptomatic":p_asymptomatic,
        "p_transmission":p_transmission,
        "incubation_period":incubation_period,
        "recovery_time":recovery_time,
        "network_type":network_type
    }


    form.form_submit_button(label="Submit")
    css="""
    <style>
        [data-testid="stForm"] {
            background:#001832;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

    # ==== end of form ====


with app_col2:
        
    # ==== generate plot ====    
    st.session_state.params = params

    fig, results_df, network_df, network_df_res = create_interactive_plot(
    st.session_state.params
    )

    st.plotly_chart(fig)


second_col1, second_col2 = st.columns([3,10], vertical_alignment="top")

with second_col1:

    with stylable_container(
        key="nx_metrics_container",
        css_styles="""
            {
                border: 0.1px solid rgba(80, 80, 80, 0.5);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                background-color: #001832;
            }
            """,
    ):
        st.write("Network Metrics")
        st.dataframe(network_df, hide_index=True, width=250)

        st.write("Network Metric Results")
        st.dataframe(network_df_res, hide_index=True, width=250)

with second_col2:

    res_fig = create_results_plot(results_df)
    st.plotly_chart(res_fig)


    with stylable_container(
            key="end_container",
            css_styles="""
                {
                    border: 0.1px solid rgba(80, 80, 80, 0.5);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    # background-color: #0E1117;
                    background-color: #001832;
                }
                """,
        ):  
        end_col1, end_col2 = st.columns([6,2])
        with end_col1:
            
            st.markdown("More info and :star: at [github.com/"
                        "pybluepanda/covid-networkx](https://github.com/"
                        "PyBluePanda/covid-networkx.git)"
            )
        with end_col2:
            button(username="samvautier", floating=False, width=221)
        



