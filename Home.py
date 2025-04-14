import streamlit as st
import os

# Page Configuration
st.set_page_config(
    page_title="Snowflake Use Case",
    page_icon="🌟",
    layout="wide",
)

# Title and Introduction
st.title("Vinod Vijayakumar - Professional Summary")
st.write(
    """
    As Director of Cloud Platform Engineering at Ford Motor Company, I lead strategic initiatives that drive 
    innovation and digital transformation in the automotive industry. With over 20 years of global experience 
    across automotive, connected vehicles, and financial services, I bring deep expertise in product development, 
    platform enablement, and project leadership.

    At Ford, I’ve led cross-functional teams to deliver scalable, cloud-native solutions and connected vehicle 
    software platforms, enabling intelligent, software-defined vehicles. My prior experience in the banking 
    and finance sector includes leading transformative programs in business process re-engineering and ERP implementations.

    I’m passionate about delivering customer value through thoughtful strategy, technology innovation, and operational excellence.
    """
)

# Core Competencies and Leadership Skills Side by Side
st.markdown("---")  # Add a horizontal divider for better styling
top_left_col, top_right_col = st.columns(2)

with top_left_col:
    st.header("Core Competencies")
    with st.expander("View Core Competencies", expanded=False):  # Collapsed by default
        st.write("""
        - Digital Transformation
        - Cloud Platforms
        - Agile and DevSecOps/SRE
        - Data Engineering
        - Program Management
        - Product Development
        - Connected Vehicle software
        - Finance & Supply Chain process
        - IT Consulting & Pre-sales
        """)

with top_right_col:
    st.header("Leadership Skills")
    with st.expander("View Leadership Skills", expanded=False):  # Collapsed by default
        st.write("""
        - Led strategic planning, budgeting, and product roadmap definition to align technology initiatives with key business outcomes and long-term growth objectives.
        - Managed diverse stakeholder groups and large cross-functional teams, driving results through effective hiring, talent development, and performance management.
        - Fostered a high-performance culture by resolving conflicts, mentoring teams, and championing continuous learning.
        - Oversaw vendor and partner relationships to ensure successful delivery, strategic alignment, and strong external collaboration.
        """)

# About Me Section with Side-by-Side Images
st.markdown("---")  # Add a horizontal divider for a clean transition
st.header("About Me")  # Updated header text
image_col1, image_col2 = st.columns(2)  # Creates two columns for images side by side

with image_col1:
    # Display the "About Me" Image
    image_path_about_me = os.path.join(os.getcwd(), "About_me.jpg")
    if os.path.exists(image_path_about_me):  # Check if the image exists
        st.image(image_path_about_me, caption="About Me", use_container_width=True)
    else:
        st.warning("The image file 'About_me.jpg' is not found in the current directory.")

with image_col2:
    # Display the "Parts of Me" Image
    image_path_parts_of_me = os.path.join(os.getcwd(), "partsofme.jpg")
    if os.path.exists(image_path_parts_of_me):  # Check if the image exists
        st.image(image_path_parts_of_me, caption="Parts of Me", use_container_width=True)
    else:
        st.warning("The image file 'partsofme.jpg' is not found in the current directory.")
