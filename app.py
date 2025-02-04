import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.buy_me_a_coffee import button
import warnings 

from model import create_interactive_plot, create_results_plot

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Covid - x - NetworkX", page_icon=":microbe:")


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

# ==== data input form ====

form = st.form(key="form_settings")
form_col1, form_col2, form_col3 = form.columns([3,3,3])

network_type = form_col1.selectbox(
    "Network Type",
    options=["small-world","scale-free","random", 
                "complete", "cycle", "lollipop"],
    key="network_type",
    placeholder="small-world"
)

N = form_col2.number_input(
    "Number of people",
    10,
    150,
    step=10,
    key="N",
    value=40
)

timesteps = form_col3.number_input(
    "Simulation steps",
    20,
    80,
    step=5,
    key="timesteps",
    value=40
)

param_expander = form.expander("Other Paramater Values:")
with param_expander:
    exp_col1, exp_col2 = param_expander.columns([3,3])

    incubation_period = exp_col1.slider(
        "Incubation period",
        1,
        10,
        step=1,
        key="incubation_period",
        value=3
    ) 

    recovery_time = exp_col2.slider(
        "Recovery time",
        1,
        10,
        step=1,
        key="recovery_time",
        value=7
    ) 

    p_asymptomatic = exp_col2.slider(
        "p_asymptomatic",
        0.0,
        1.0,
        step=.1,
        key="p_asymptomatic",
        value=0.3
    ) 

    p_transmission = exp_col1.slider(
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
    :orange[Exposed] /
    Asymptomatic spreaders / 
    :red[Infected (symptomatic)] /
    :green[Recovered]
    ''')
        
# ==== generate plot ====    
st.session_state.params = params

fig, results_df, network_df, network_df_res = create_interactive_plot(
st.session_state.params
)

st.plotly_chart(fig)


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
    net1, net2 = st.columns([3,3])

    with net1:
        st.write("Network Metrics")
        st.dataframe(network_df, hide_index=True, width=250)
    with net2:
        st.write("Network Metric Results")
        st.dataframe(network_df_res, hide_index=True, width=250)


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
    end_col1, end_col2 = st.columns([4,2])
    with end_col1:
        
        st.markdown("More info and :star: at [github.com/"
                    "pybluepanda/covid-networkx](https://github.com/"
                    "PyBluePanda/covid-networkx.git)"
        )
    with end_col2:
        button(username="samvautier", floating=False, width=221)
        



