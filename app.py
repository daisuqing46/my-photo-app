import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="AI 专业证件照", layout="centered")
st.title("✨ AI 专业证件照生成器")

# 1. 定义标准尺寸（宽, 高）以像素为单位
size_dict = {
    "原始比例": None,
    "一寸 (295x413 px)": (295, 413),
    "二寸 (413x579 px)": (413, 579),
    "考研/英语四六级 (480x640 px)": (480, 640)
}

# 2. 侧边栏配置
st.sidebar.header("参数设置")
target_size_name = st.sidebar.selectbox("选择证件尺寸", list(size_dict.keys()))
bg_color = st.sidebar.color_picker('选择背景颜色', '#0000FF')

uploaded_file = st.file_uploader("请上传一张生活照...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption='原图', use_container_width=True)

    if st.button('开始制作'):
        with st.spinner('AI 正在发力...'):
            # 3. 抠图
            output_image = remove(input_image)
            
            # 4. 填充背景
            new_bg = Image.new("RGBA", output_image.size, bg_color)
            new_bg.paste(output_image, (0, 0), mask=output_image)
            result_img = new_bg.convert("RGB")
            
            # 5. 尺寸裁剪逻辑
            target_size = size_dict[target_size_name]
            if target_size:
                # 保持比例裁剪 (Crop)
                result_img.thumbnail((target_size[0] * 2, target_size[1] * 2)) # 先缩放
                result_img = result_img.resize(target_size, Image.Resampling.LANCZOS)
            
            st.success(f"制作完成！尺寸：{target_size_name}")
            st.image(result_img, caption='生成效果', use_container_width=False)
            
            # 6. 下载
            buf = io.BytesIO()
            result_img.save(buf, format="JPEG", quality=95)
            st.download_button(
                label="保存到电脑",
                data=buf.getvalue(),
                file_name=f"zhengjianzhao_{target_size_name}.jpg",
                mime="image/jpeg"
            )