import streamlit as st
from rembg import remove
from PIL import Image
import io

# 1. 网页基础配置
st.set_page_config(page_title="AI 专业证件照", layout="centered")
st.title("✨ AI 专业证件照（商业演示版）")

# 2. 定义标准尺寸（宽, 高）
size_dict = {
    "原始比例": None,
    "一寸 (295x413 px)": (295, 413),
    "二寸 (413x579 px)": (413, 579),
    "考研/英语四六级 (480x640 px)": (480, 640)
}

# 3. 侧边栏：参数设置
st.sidebar.header("🎨 制作设置")
target_size_name = st.sidebar.selectbox("第一步：选择证件尺寸", list(size_dict.keys()))
bg_color = st.sidebar.color_picker('第二步：选择背景颜色', '#0000FF') # 默认蓝色

# 4. 主界面：上传文件
uploaded_file = st.file_uploader("第三步：上传一张生活照...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption='已上传的原图', use_container_width=True)

    if st.button('🚀 开始制作（免费预览）'):
        with st.spinner('AI 正在抠图换底，请稍候...'):
            # 执行抠图
            output_image = remove(input_image)
            
            # 填充背景
            new_bg = Image.new("RGBA", output_image.size, bg_color)
            new_bg.paste(output_image, (0, 0), mask=output_image)
            result_img = new_bg.convert("RGB")
            
            # 尺寸裁剪逻辑
            target_size = size_dict[target_size_name]
            if target_size:
                result_img = result_img.resize(target_size, Image.Resampling.LANCZOS)
            
            # 展示预览图（加水印或者缩小展示，这里直接展示）
            st.success(f"✅ 预览制作完成！尺寸：{target_size_name}")
            st.image(result_img, caption='生成效果预览', use_container_width=False)
            
            # --- 💰 收费解锁模块 ---
            st.write("---")
            st.subheader("📥 下载高清无水印成品")
            
            col1, col2 = st.columns(2)
            with col1:
                # 这里的 pay.png 必须是你上传到 GitHub 的收款码文件名
                st.image("pay.png", caption="扫码支付 2 元获取解锁暗号", width=200)
            
            with col2:
                st.write("👉 **获取方式：**")
                st.write("1. 扫码支付 2 元并备注：证件照")
                st.write("2. 加微信：**Linsuqing1995** (或设置固定暗号)")
                
                # 设置一个暗号输入框