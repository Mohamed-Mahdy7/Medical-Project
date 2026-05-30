
function InputField({
    id, label, type, placeholder,
    value, onChange, className, setValue
}){
    return (
        <div>
            <label htmlFor={id}>{label}</label>
            <input 
                id={id}
                type={type}
                placeholder={placeholder}
                value={value}
                className={className}
                onChange={(e) => setValue(e.target.value)}
                required
            />
        </div>
    );
}

export default InputField;