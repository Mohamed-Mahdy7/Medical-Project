function AdminButton() {
    return (
        <button
            className="btn-ghost"
            style={{width: "100%"}}
            onClick={() => {
                window.location.replace("http://localhost:8000/admin/");
            }}
        >
            Admin Panel
        </button>
    );
}

export default AdminButton