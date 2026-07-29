from django import forms

class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.txt'})
    )
    resume_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Or paste resume text here...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('resume_file') and not cleaned_data.get('resume_text'):
            raise forms.ValidationError("Please upload a file or paste resume text.")
        return cleaned_data